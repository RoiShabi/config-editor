#!/usr/bin/env python3

import sys
import shutil
import pathlib
import unittest
import filecmp
import io
from contextlib import redirect_stdout


root_dir = str(pathlib.Path(__file__).parent.parent)
sys.path.insert(0, root_dir)
from config_editor import main as subject_main


TEST_TEMP_DIR = root_dir+"/test/temp"
TEST_CASES_DIR = root_dir+"/test/test_cases"
TEST_EXPECTED_RESULTS_DIR = root_dir+"/test/test_expected_results"
TEST_SUBJECT_FILE = root_dir+"main.py"

class MainTest(unittest.TestCase):
    def test_no_args_inprocess(self):
        errcode = subject_main([TEST_SUBJECT_FILE])
        self.assertNotEqual(errcode, 0)

    def test_help_flag(self):
        captured_stdout = io.StringIO()
        with redirect_stdout(captured_stdout):
            result = subject_main([TEST_SUBJECT_FILE, '--help'])
            self.assertEqual(result, 0)
        out_buff = captured_stdout.getvalue()
        self.assertIn('Usage', out_buff)

    def test_append_nohz_full(self):
        test_file = TEST_TEMP_DIR+"/test_append_nohz_full"
        test_source_file = TEST_CASES_DIR+"/grub_exist_isolcpu"
        test_expected_result = TEST_EXPECTED_RESULTS_DIR+"/grub_append_nohz_full"
        shutil.copy(test_source_file, test_file)
        result = subject_main([TEST_SUBJECT_FILE, f'file={test_file}', 'field=GRUB_CMDLINE_LINUX_DEFAULT', 'key=nohz_full', 'value=0,1,2', 'accept=yes'])
        self.assertTrue(filecmp.cmp(test_file, test_expected_result) )
        pathlib.Path.unlink(test_file)

    def test_append_isolcpu_specific_element(self):
        test_file = TEST_TEMP_DIR+"/test_append_isolcpu_specific_element"
        test_source_file = TEST_CASES_DIR+"/grub_exist_isolcpu"
        test_expected_result = TEST_EXPECTED_RESULTS_DIR+"/grub_append_isolcpu_elements"
        shutil.copy(test_source_file, test_file)
        result = subject_main([TEST_SUBJECT_FILE, f'file={test_file}', 'field=GRUB_CMDLINE_LINUX_DEFAULT', 'key=isolcpu', 'value=3', 'accept=yes'])
        self.assertTrue(filecmp.cmp(test_file, test_expected_result) )
        pathlib.Path.unlink(test_file)

    def test_do_nothing_isolcpu_element_exist(self):
        test_file = TEST_TEMP_DIR+"/test_do_nothing_isolcpu_element_exist"
        test_source_file = TEST_CASES_DIR+"/grub_exist_isolcpu"
        shutil.copy(test_source_file, test_file)
        result = subject_main([TEST_SUBJECT_FILE, f'file={test_file}', 'field=GRUB_CMDLINE_LINUX_DEFAULT', 'key=isolcpu', 'value=0', 'accept=yes'])
        self.assertTrue(filecmp.cmp(test_file, test_source_file) )
        pathlib.Path.unlink(test_file)

    def test_append_ldlibpath(self):
        test_file = TEST_TEMP_DIR+"/test_append_ldlibpath"
        test_source_file = TEST_CASES_DIR+"/environment_exist_path_missing_ldlibpath"
        test_expected_result = TEST_EXPECTED_RESULTS_DIR+"/environment_append_ldlibpath_with_value"
        shutil.copy(test_source_file, test_file)
        result = subject_main([TEST_SUBJECT_FILE, f'file={test_file}', 'field=LD_LIBRARY_PATH', 'value=/usr/local/lib', 'delimiter=:', 'accept=yes'])
        self.assertTrue(filecmp.cmp(test_file, test_expected_result) )
        pathlib.Path.unlink(test_file)

    def test_append_path(self):
        test_file = TEST_TEMP_DIR+"/test_append_path"
        test_source_file = TEST_CASES_DIR+"/environment_exist_path_missing_ldlibpath"
        test_expected_result = TEST_EXPECTED_RESULTS_DIR+"/environment_append_path"
        shutil.copy(test_source_file, test_file)
        result = subject_main([TEST_SUBJECT_FILE, f'file={test_file}', 'field=PATH', 'value=/usr/local/cuda/bin', 'delimiter=:', 'accept=yes'])
        self.assertTrue(filecmp.cmp(test_file, test_expected_result) )
        pathlib.Path.unlink(test_file)


if __name__ == '__main__':
    temp_path = pathlib.Path(TEST_TEMP_DIR)
    temp_path.mkdir(exist_ok=True)
    unittest.main()
    temp_path.rmdir()
