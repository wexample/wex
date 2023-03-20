import os
import unittest
import shutil
from src.core.Kernel import Kernel
from src.core.action.TestCoreAction import TestCoreAction


class AbstractTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kernel = Kernel(os.getcwd() + '/__main__.py')
        cls.kernel.setup_test_manager(
            TestCoreAction(cls.kernel)
        )

    def assertFileExists(self, file_path, exists=True):
        """
        Assert that the specified file exists.
        """
        self.assertEqual(
            os.path.exists(file_path),
            exists,
            f'The file does not exists : {file_path}'
        )

    def build_test_file_path(self, fine_name) -> str:
        dst_file = self.kernel.path['tmp'] + 'tests/' + fine_name

        shutil.copy2(
            self.kernel.path['root'] + 'tests/samples/' + fine_name,
            dst_file)

        return dst_file
