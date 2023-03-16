import os
import unittest
from src.core.Kernel import Kernel

class AbstractTestCase(unittest.TestCase):
    def setUp(self):
        self.kernel = Kernel(os.getcwd() + '/__main__.py')
