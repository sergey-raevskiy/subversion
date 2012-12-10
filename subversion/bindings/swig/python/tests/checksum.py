#
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
#
import unittest, setup_path
import svn.core

class ChecksumTestCases(unittest.TestCase):
    def test_checksum(self):
        # Checking primarily the return type for the svn_checksum_create
        # function
        val = svn.core.svn_checksum_create(svn.core.svn_checksum_md5)
        check_val = svn.core.svn_checksum_to_cstring_display(val)

        # The svn_checksum_to_cstring_display should return a str type object
        # from the check_val object passed to it
        if(type(check_val) == str):
            # The intialized value created from a checksum should be 0
            if(int(check_val) != 0):
                self.assertRaises(AssertionError)
        else:
            self.assertRaises(TypeError, test_checksum)

def suite():
    return unittest.defaultTestLoader.loadTestsFromTestCase(ChecksumTestCases)
if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
    


