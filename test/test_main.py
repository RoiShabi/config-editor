#!/usr/bin/env python3

import sys
import shutil
import pathlib
import unittest
import filecmp

root_dir = str(pathlib.Path(__file__).parent.parent)
sys.path.insert(0, root_dir)
from main import main as subject_main


TEST_TEMP_DIR = root_dir+"/test/temp"
TEST_CASES_DIR = root_dir+"/test/test_cases"
TEST_EXPECTED_RESULTS_DIR = root_dir+"/test/test_expected_results"
TEST_SUBJECT_FILE = root_dir+"main.py"

class MainTest(unittest.TestCase):
    def test_no_args_inprocess(self):
        with self.assertRaises(TypeError) as cm:
            subject_main([TEST_SUBJECT_FILE])

    # def test_help_flag(self):
    #     result = subject_main(['--help'])
    #     # TODO: assert that help message is shown
    #     # e.g.:
    #     self.assertEqual(result.returncode, 0)
    #     self.assertIn('Usage', result.stdout)

    # def test_additional_option(self):
    #     result = subject_main(['--verbose'])
    #     # TODO: assert verbose output behavior
    #     # e.g.:
    #     # self.assertEqual(result.returncode, 0)
    #     # self.assertIn('Verbose mode enabled', result.stdout)

    def test_append_nohz_full(self):
        test_file = TEST_TEMP_DIR+"/test_append_nohz_full"
        test_source_file = TEST_CASES_DIR+"/grub_exist_isolcpu"
        test_expected_result = TEST_EXPECTED_RESULTS_DIR+"/grub_append_nohz_full"
        shutil.copy(test_source_file, test_file)
        result = subject_main([TEST_SUBJECT_FILE, f'file={test_file}', 'field=GRUB_CMDLINE_LINUX_DEFAULT', 'key=nohz_full', 'value=0,1,2'])
        self.assertTrue(filecmp.cmp(test_file, test_expected_result) )
        pathlib.Path.unlink(test_file)

    def test_append_ldlibpath(self):
        test_file = TEST_TEMP_DIR+"/test_append_ldlibpath"
        test_source_file = TEST_CASES_DIR+"/environment_exist_path_missing_ldlibpath"
        test_expected_result = TEST_EXPECTED_RESULTS_DIR+"/environment_append_ldlibpath_with_value"
        shutil.copy(test_source_file, test_file)
        result = subject_main([TEST_SUBJECT_FILE, f'file={test_file}', 'field=LD_LIBRARY_PATH', 'value=/usr/local/lib', 'delimiter=:'])
        self.assertTrue(filecmp.cmp(test_file, test_expected_result) )
        pathlib.Path.unlink(test_file)

    def test_append_path(self):
        test_file = TEST_TEMP_DIR+"/test_append_path"
        test_source_file = TEST_CASES_DIR+"/environment_exist_path_missing_ldlibpath"
        test_expected_result = TEST_EXPECTED_RESULTS_DIR+"/environment_append_path"
        shutil.copy(test_source_file, test_file)
        result = subject_main([TEST_SUBJECT_FILE, f'file={test_file}', 'field=PATH', 'value=/usr/local/cuda/bin', 'delimiter=:'])
        self.assertTrue(filecmp.cmp(test_file, test_expected_result) )
        pathlib.Path.unlink(test_file)


if __name__ == '__main__':
    temp_path = pathlib.Path(TEST_TEMP_DIR)
    temp_path.mkdir(exist_ok=True)
    unittest.main()
    temp_path.rmdir()
