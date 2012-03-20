#  See http://subversion.tigris.org for more information.
# Copyright (c) 2000-2008 CollabNet.  All rights reserved.
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.  The terms
# are also available at http://subversion.tigris.org/license-1.html.
# If newer versions of this license are posted there, you may use a
# newer version instead, at your option.
import sys, re, os, time
Skip = svntest.testcase.Skip
XFail = svntest.testcase.XFail
# ### TODO: directory delete doesn't work yet
#  repo_diff(wc_dir, 1, 4, check_add_a_file_in_a_subdir_reverse)
  expected_output = [
    "\n",
    "Property changes on: iota\n",
    "___________________________________________________________________\n",
    "Added: svn:eol-style\n",
    "   + native\n",
    "\n" ]
  expected_reverse_output = list(expected_output)
  expected_reverse_output[3] = expected_reverse_output[3].replace("Added",
                                                                  "Deleted")
  expected_reverse_output[4] = "   - native\n"
  svntest.actions.run_and_verify_svn(None, expected_output, [],
  svntest.actions.run_and_verify_svn(None, expected_output, [],

  theta_contents = svntest.main.file_read(
    os.path.join(sys.path[0], "theta.bin"), 'rb')

  if list1 != list2:
    raise svntest.Failure

  regex = 'svn: Unable to find repository location for \'.*\''
  for line in err_output:
    if re.match(regex, line):
      break
  else:
  for line in err_output:
    if re.match(regex, line):
      break
  else:
  regex = 'svn: \'.*\' was not found in the repository'
  for line in err_output:
    if re.match(regex, line):
      break
  else:
  "diff between two file URLs (issue #1311)"
  verify_expected_output(out, "   + pvalue")
  verify_expected_output(out, "   + pvalue")  # fails at r7481
  verify_expected_output(out, "   + pvalue")
                       'M') :
  # Repos->WC of the directory
  # Repos->WC diff of file after the rename.
  # Repos->repos diff after the rename.
  verify_expected_output(diff_output, "   - v")
    None, 'diff', os.path.join('A', 'D'))
  # Test the diff while within the moved directory
  os.chdir(os.path.join('A','D','I'))
  if check_diff_output(diff_output, 'pi', 'A') :
  # Test a repos->repos diff while within the moved directory
  if check_diff_output(diff_output, 'pi', 'A') :
  expected_output_r1_r2 = [
    "\n",
    "Property changes on: A\n",
    "___________________________________________________________________\n",
    "Added: dirprop\n",
    "   + r2value\n",
    "\n",
    "\n",
    "Property changes on: iota\n",
    "___________________________________________________________________\n",
    "Added: fileprop\n",
    "   + r2value\n",
    "\n" ]

  expected_output_r2_r1 = list(expected_output_r1_r2)
  expected_output_r2_r1[3] = expected_output_r2_r1[3].replace("Added",
                                                              "Deleted")
  expected_output_r2_r1[4] = "   - r2value\n"
  expected_output_r2_r1[9] = expected_output_r2_r1[9].replace("Added",
                                                              "Deleted")
  expected_output_r2_r1[10] = "   - r2value\n"
  expected = svntest.verify.UnorderedOutput(expected_output_r1_r2)
  expected = svntest.verify.UnorderedOutput(expected_output_r2_r1)
  # presence of local mods.
  expected = svntest.verify.UnorderedOutput(expected_output_r1_r2)
  expected = svntest.verify.UnorderedOutput(expected_output_r2_r1)
                                                "revision 3") + [
  expected_output_r2_wc = [
    "\n",
    "Property changes on: A\n",
    "___________________________________________________________________\n",
    "Modified: dirprop\n",
    "   - r2value\n",
    "   + workingvalue\n",
    "Added: newdirprop\n",
    "   + newworkingvalue\n",
    "\n",
    "\n",
    "Property changes on: iota\n",
    "___________________________________________________________________\n",
    "Modified: fileprop\n",
    "   - r2value\n",
    "   + workingvalue\n",
    "Added: newfileprop\n",
    "   + newworkingvalue\n",
    "\n" ]
  expected_output_r1_r3 = make_diff_header("foo", "revision 0",
                                                "revision 3") + [
    "\n",
    "Property changes on: foo\n",
    "___________________________________________________________________\n",
    "Added: propname\n",
    "   + propvalue\n",
    "\n",
    "\n",
    "Property changes on: X\n",
    "___________________________________________________________________\n",
    "Added: propname\n",
    "   + propvalue\n",
    "\n",
  ] + make_diff_header("X/bar", "revision 0", "revision 3") + [
    "\n",
    "Property changes on: " + os.path.join('X', 'bar') + "\n",
    "___________________________________________________________________\n",
    "Added: propname\n",
    "   + propvalue\n",
    "\n" ]
  # The output from the BASE->repos diff is the same content, but in a
  # different order.
  expected_output_r1_r3_a = expected_output_r1_r3[:12] + \
    expected_output_r1_r3[18:] + expected_output_r1_r3[12:18]
  svntest.actions.run_and_verify_svn(None, expected_output_r1_r3, [],
  svntest.actions.run_and_verify_svn(None, expected_output_r1_r3, [],
  svntest.actions.run_and_verify_svn(None, expected_output_r1_r3_a, [],
  # Check that a base->repos diff shows deleted and added lines.
  # It's not clear whether we expect a file-change diff or
  # a file-delete plus file-add.  The former is currently produced if we
  # explicitly request a diff of the file itself, and the latter if we
  # request a tree diff which just happens to contain the file.

  # A content modification.
  svntest.main.file_append(os.path.join(wc_dir, "A", "mu"), "New mu content")
  # A prop modification.
  svntest.main.run_svn(None,
                       "propset", "prop", "val",
                       os.path.join(wc_dir, 'iota'))
  tau_path = os.path.join(wc_dir, "A", "D", "G", "tau")
  svntest.main.file_append(tau_path, "tautau")
  svntest.main.run_svn(None,
                       "propset", "prop", "val", tau_path)

  # A file addition.
  newfile_path = os.path.join(wc_dir, 'newfile')
  svntest.main.file_append(newfile_path, 'newfile')
  svntest.main.run_svn(None, 'add', newfile_path)

  # A file deletion.
  svntest.main.run_svn(None, "delete", os.path.join(wc_dir, 'A', 'B',
                                                    'lambda'))

  expected_output = svntest.wc.State(wc_dir, {
    'A/mu': Item(verb='Sending'),
    'iota': Item(verb='Sending'),
    'newfile': Item(verb='Adding'),
    'A/D/G/tau': Item(verb='Sending'),
    'A/B/lambda': Item(verb='Deleting'),
    })
  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.add({
    'newfile': Item(status='  ', wc_rev=2),
    })
  expected_status.tweak("A/mu", "iota", "A/D/G/tau", 'newfile', wc_rev=2)
  expected_status.remove("A/B/lambda")

  svntest.actions.run_and_verify_commit(wc_dir, expected_output,
                                        expected_status, None, wc_dir)
  svntest.actions.run_and_verify_diff_summarize(expected_diff, None,
                                                None, None, None, None,
                                                os.path.join(wc_dir, 'iota'),
                                                '-c2')
  # Get the differences between two versions of an entire directory.
    'A/mu': Item(status='M '),
    'iota': Item(status=' M'),
    'A/D/G/tau': Item(status='MM'),
    'newfile': Item(status='A '),
    'A/B/lambda': Item(status='D '),
  svntest.actions.run_and_verify_diff_summarize(expected_diff, None,
                                                None, None, None, None,
                                                wc_dir, '-r1:2')

  diff = [
    "\n",
    "Property changes on: .\n",
    "___________________________________________________________________\n",
    "Added: foo1\n",
    "   + bar1\n",
    "\n",
    "\n",
    "Property changes on: iota\n",
    "___________________________________________________________________\n",
    "Added: foo2\n",
    "   + bar2\n",
    "\n",
    "\n",
    "Property changes on: A\n",
    "___________________________________________________________________\n",
    "Added: foo3\n",
    "   + bar3\n",
    "\n",
    "\n",
    "Property changes on: " + os.path.join('A', 'B') + "\n",
    "___________________________________________________________________\n",
    "Added: foo4\n",
    "   + bar4\n",
    "\n" ]

  expected_empty = svntest.verify.UnorderedOutput(diff[:6])
  expected_files = svntest.verify.UnorderedOutput(diff[:12])
  expected_immediates = svntest.verify.UnorderedOutput(diff[:18])
  expected_infinity = svntest.verify.UnorderedOutput(diff[:])
  # Test repos-repos diff.  Reuse the expected outputs from above.
  diff_wc_repos = [
    "\n",
    "Property changes on: .\n",
    "___________________________________________________________________\n",
    "Modified: foo1\n",
    "   - bar1\n",
    "   + baz1\n",
    "\n",
    "\n",
    "Property changes on: iota\n",
    "___________________________________________________________________\n",
    "Modified: foo2\n",
    "   - bar2\n",
    "   + baz2\n",
    "\n",
    "\n",
    "Index: iota\n",
    "===================================================================\n",
    "--- iota\t(revision 2)\n",
    "+++ iota\t(working copy)\n",
    "Property changes on: A\n",
    "___________________________________________________________________\n",
    "Modified: foo3\n",
    "   - bar3\n",
    "   + baz3\n",
    "\n",
    "\n",
    "Property changes on: " + os.path.join('A', 'B') + "\n",
    "___________________________________________________________________\n",
    "Modified: foo4\n",
    "   - bar4\n",
    "   + baz4\n",
    "\n",
    "Index: A/mu\n",
    "===================================================================\n",
    "--- A/mu\t(revision 1)\n",
    "+++ A/mu\t(working copy)\n",
    "@@ -1 +1,2 @@\n",
    " This is the file 'mu'.\n",
    "+new text\n" ]

  expected_empty = svntest.verify.UnorderedOutput(diff_wc_repos[:7])
  expected_files = svntest.verify.UnorderedOutput(diff_wc_repos[1:22])
  expected_immediates = svntest.verify.UnorderedOutput(diff_wc_repos[1:29])
  time.sleep(1)
  # 3) Test working copy summarize
  svntest.actions.run_and_verify_diff_summarize_xml(
    ".*Summarizing diff can only compare repository to repository",
    None, wc_dir, None, None, wc_dir)

  paths = ['iota',]
  items = ['none',]
  kinds = ['file',]
  props = ['modified',]
    [], wc_dir, paths, items, props, kinds, '-c2',
  paths = ['A/mu', 'iota', 'A/D/G/tau', 'newfile', 'A/B/lambda',
           'newdir',]
  items = ['modified', 'none', 'modified', 'added', 'deleted', 'added',]
  kinds = ['file','file','file','file','file', 'dir',]
  props = ['none', 'modified', 'modified', 'none', 'none', 'none',]

  paths = ['A/mu', 'iota', 'A/D/G/tau', 'newfile', 'A/B/lambda',
           'newdir',]
  items = ['modified', 'none', 'modified', 'added', 'deleted', 'added',]
  kinds = ['file','file','file','file','file', 'dir',]
  props = ['none', 'modified', 'modified', 'none', 'none', 'none',]

  expected_error = "(.*svn: Invalid argument .* in diff options.*)|" \
                   "(svn: '.' is not a working copy)"
  svntest.actions.run_and_verify_svn(None, [], expected_error,
    'for arg in sys.argv[1:]:\n  print arg\n')
    os.path.join('.svn', 'text-base', 'iota.svn-base') + "\n",
    "iota\n"])
# Diff rev against working copy of a removed and locally re-added file.
# This is issue #1675 ("svn diff -rN added-file" has odd behavior).

  "diff -r1 of removed file to its local addition"
              XFail(diff_renamed_dir),
              XFail(diff_url_against_local_mods),
              XFail(diff_preexisting_rev_against_local_add),