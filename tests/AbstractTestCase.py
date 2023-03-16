import os
import unittest
from src.core.Kernel import Kernel

class AbstractTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kernel = Kernel(os.getcwd() + '/__main__.py')
        cls.kernel.setup_test_manager()
