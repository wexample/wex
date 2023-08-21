import os
import unittest
from src.core.Kernel import Kernel
from src.core.action.TestCoreAction import TestCoreAction
from src.helper.file import create_directories_and_copy


class AbstractTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kernel = Kernel(os.getcwd() + '/__main__.py')
        cls.kernel.setup_test_manager(
            TestCoreAction(cls.kernel)
        )

    def setUp(self):
        # Add a new line between each test
        self.kernel.print("")

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
