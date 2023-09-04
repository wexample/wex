import os
import unittest

from src.core.TestKernel import TestKernel
from src.helper.file import create_directories_and_copy


class AbstractTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kernel = TestKernel(os.getcwd() + '/__main__.py')

    def setUp(self):
        # Add a new line between each test
        self.kernel.print("")

        self.test_dir = os.getcwd()

    def tearDown(self):
        # Add a new line between each test
        self.kernel.print("")

        # If workdir changed.
        current_dir = os.getcwd()
        if current_dir != self.test_dir:
            self.kernel.log(f'Reset working directory to : {self.test_dir}')

            os.chdir(self.test_dir)

    def assertPathExists(self, file_path, exists=True):
        """
        Assert that the specified file exists.
        """
        self.assertEqual(
            os.path.exists(file_path),
            exists,
            f'No such file or directory : {file_path}'
        )

    def build_test_file_path(self, file_name: str) -> str:
        src_file = os.path.join(self.kernel.path['root'], 'tests', 'samples', file_name)
        dst_file = os.path.join(self.kernel.path['tmp'], 'tests', file_name)

        # Use the function to create directories and copy the file
        create_directories_and_copy(src_file, dst_file)

        return dst_file
