/* low_level.c --- low level r/w access to fs_fs file structures
 *
 * ====================================================================
 *    Licensed to the Apache Software Foundation (ASF) under one
 *    or more contributor license agreements.  See the NOTICE file
 *    distributed with this work for additional information
 *    regarding copyright ownership.  The ASF licenses this file
 *    to you under the Apache License, Version 2.0 (the
 *    "License"); you may not use this file except in compliance
 *    with the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *    Unless required by applicable law or agreed to in writing,
 *    software distributed under the License is distributed on an
 *    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 *    KIND, either express or implied.  See the License for the
 *    specific language governing permissions and limitations
 *    under the License.
 * ====================================================================
 */

#include "svn_fs.h"

#include "fs_fs.h"
#include "id.h"

/* Headers used to describe node-revision in the revision file. */
#define HEADER_ID          "id"
#define HEADER_TYPE        "type"
#define HEADER_COUNT       "count"
#define HEADER_PROPS       "props"
#define HEADER_TEXT        "text"
#define HEADER_CPATH       "cpath"
#define HEADER_PRED        "pred"
#define HEADER_COPYFROM    "copyfrom"
#define HEADER_COPYROOT    "copyroot"
#define HEADER_FRESHTXNRT  "is-fresh-txn-root"
#define HEADER_MINFO_HERE  "minfo-here"
#define HEADER_MINFO_CNT   "minfo-cnt"

/* Kinds that a change can be. */
#define ACTION_MODIFY      "modify"
#define ACTION_ADD         "add"
#define ACTION_DELETE      "delete"
#define ACTION_REPLACE     "replace"
#define ACTION_RESET       "reset"

/* True and False flags. */
#define FLAG_TRUE          "true"
#define FLAG_FALSE         "false"

/* Kinds that a node-rev can be. */
#define KIND_FILE          "file"
#define KIND_DIR           "dir"

/* Kinds of representation. */
#define REP_PLAIN          "PLAIN"
#define REP_DELTA          "DELTA"

/* An arbitrary maximum path length, so clients can't run us out of memory
 * by giving us arbitrarily large paths. */
#define FSFS_MAX_PATH_LEN 4096

/* Given the last "few" bytes (should be at least 40) of revision REV in
 * TRAILER,  parse the last line and return the offset of the root noderev
 * in *ROOT_OFFSET and the offset of the changes list in *CHANGES_OFFSET.
 * All offsets are relative to the revision's start offset.
 * 
 * Note that REV is only used to construct nicer error objects.
 */
svn_error_t *
parse_revision_trailer(apr_off_t *root_offset,
                       apr_off_t *changes_offset,
                       svn_stringbuf_t *trailer,
                       svn_revnum_t rev);

/* Given the offset of the root noderev in ROOT_OFFSET and the offset of
 * the changes list in CHANGES_OFFSET,  return the corresponding revision's
 * trailer.  Allocate it in POOL.
 */
svn_stringbuf_t *
unparse_revision_trailer(apr_off_t root_offset,
                         apr_off_t changes_offset,
                         apr_pool_t *pool);

/* Given a revision file FILE that has been pre-positioned at the
   beginning of a Node-Rev header block, read in that header block and
   store it in the apr_hash_t HEADERS.  All allocations will be from
   POOL. */
svn_error_t *
read_header_block(apr_hash_t **headers,
                  svn_stream_t *stream,
                  apr_pool_t *pool);

/* Parse the description of a representation from STRING and store it
   into *REP_P.  If the representation is mutable (the revision is
   given as -1), then use TXN_ID for the representation's txn_id
   field.  If MUTABLE_REP_TRUNCATED is true, then this representation
   is for property or directory contents, and no information will be
   expected except the "-1" revision number for a mutable
   representation.  Allocate *REP_P in POOL. */
svn_error_t *
read_rep_offsets_body(representation_t **rep_p,
                      char *string,
                      const char *txn_id,
                      svn_boolean_t mutable_rep_truncated,
                      apr_pool_t *pool);

/* Wrap read_rep_offsets_body(), extracting its TXN_ID from our NODEREV_ID,
   and adding an error message. */
svn_error_t *
read_rep_offsets(representation_t **rep_p,
                 char *string,
                 const svn_fs_id_t *noderev_id,
                 svn_boolean_t mutable_rep_truncated,
                 apr_pool_t *pool);

/* Write the node-revision NODEREV into the stream OUTFILE, compatible with
   filesystem format FORMAT.  Only write mergeinfo-related metadata if
   INCLUDE_MERGEINFO is true.  Temporary allocations are from POOL. */
svn_error_t *
svn_fs_fs__write_noderev(svn_stream_t *outfile,
                         node_revision_t *noderev,
                         int format,
                         svn_boolean_t include_mergeinfo,
                         apr_pool_t *pool);

/* Read a node-revision from STREAM. Set *NODEREV to the new structure,
   allocated in POOL. */
svn_error_t *
svn_fs_fs__read_noderev(node_revision_t **noderev,
                        svn_stream_t *stream,
                        apr_pool_t *pool);

/* Return a formatted string, compatible with filesystem format FORMAT,
   that represents the location of representation REP.  If
   MUTABLE_REP_TRUNCATED is given, the rep is for props or dir contents,
   and only a "-1" revision number will be given for a mutable rep.
   If MAY_BE_CORRUPT is true, guard for NULL when constructing the string.
   Perform the allocation from POOL.  */
const char *
representation_string(representation_t *rep,
                      int format,
                      svn_boolean_t mutable_rep_truncated,
                      svn_boolean_t may_be_corrupt,
                      apr_pool_t *pool);

/* This structure is used to hold the information associated with a
   REP line. */
typedef struct rep_args_t
{
  svn_boolean_t is_delta;
  svn_boolean_t is_delta_vs_empty;

  svn_revnum_t base_revision;
  apr_off_t base_offset;
  svn_filesize_t base_length;
} rep_args_t;

/* Read the next line from file FILE and parse it as a text
   representation entry.  Return the parsed entry in *REP_ARGS_P.
   Perform all allocations in POOL. */
svn_error_t *
read_rep_line(rep_args_t **rep_args_p,
              svn_stream_t *stream,
              apr_pool_t *pool);

svn_error_t *
write_rep_line(rep_args_t *rep_args,
               svn_stream_t *stream,
               apr_pool_t *pool);


/* Fetch all the changes from FILE and store them in *CHANGES.  Do all
   allocations in POOL. */
svn_error_t *
read_all_changes(apr_array_header_t **changes,
                 apr_file_t *file,
                 apr_pool_t *pool);

/* Write a single change entry, path PATH, change CHANGE, and copyfrom
   string COPYFROM, into the file specified by FILE.  Only include the
   node kind field if INCLUDE_NODE_KIND is true.  All temporary
   allocations are in POOL. */
svn_error_t *
write_change_entry(svn_stream_t *stream,
                   const char *path,
                   svn_fs_path_change2_t *change,
                   svn_boolean_t include_node_kind,
                   apr_pool_t *pool);

/* Write the changed path info from transaction TXN_ID in filesystem
   FS to the permanent rev-file FILE.  *OFFSET_P is set the to offset
   in the file of the beginning of this information.  Perform
   temporary allocations in POOL. */
svn_error_t *
write_changed_path_info(svn_stream_t *stream,
                        svn_fs_t *fs,
                        apr_hash_t *changed_paths,
                        apr_pool_t *pool);

svn_error_t *
get_root_changes_offset(apr_off_t *root_offset,
                        apr_off_t *changes_offset,
                        apr_file_t *rev_file,
                        svn_fs_t *fs,
                        svn_revnum_t rev,
                        apr_pool_t *pool);