import os
import unittest
from unittest.mock import patch

import cycle_checker

FIXTURES = './tests/fixtures'


class TestFileOpener(unittest.TestCase):

    def setUp(self) -> None:
        self.fixtures_path = FIXTURES

    def test_existing_file_opens_and_serializes(self):
        for el in os.listdir(self.fixtures_path):
            r = cycle_checker.get_config(os.path.join(self.fixtures_path, el))
            self.assertIsInstance(r, dict)

    def test_non_existing_file_raise_error(self):
        with self.assertRaises(FileNotFoundError):
            cycle_checker.get_config('some_fictional_file.txt')


class TestMainLogic(unittest.TestCase):

    def setUp(self):
        files = os.listdir(FIXTURES)
        self.good = [
            os.path.join(FIXTURES, f) for f in files if f.startswith('true')
        ]
        self.bad = [
            os.path.join(FIXTURES, f) for f in files if f.startswith('false')
        ]

    @patch('cycle_checker.get_config')
    def test_bare_check_return_true(self, mock):
        mock.return_value = {"1": [2, 3, 4]}
        r = cycle_checker.main('hello.json')
        self.assertTrue(r)

    @patch('cycle_checker.get_config')
    def test_bare_check_return_false(self, mock):
        mock.return_value = {"1": [1]}
        r = cycle_checker.main('hello.json')
        self.assertFalse(r)

    def test_good_files_return_true(self):
        for f in self.good:
            with self.subTest(f=f):
                r = cycle_checker.main(f)
                self.assertTrue(r)

    def test_bad_files_return_false(self):
        for f in self.bad:
            with self.subTest(f=f):
                r = cycle_checker.main(f)
                self.assertFalse(r)
