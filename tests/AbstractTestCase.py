import os
import unittest
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
