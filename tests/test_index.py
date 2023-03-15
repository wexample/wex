import os.path
import unittest
from src.core.Kernel import Kernel


class TestIndex(unittest.TestCase):
    def setUp(self):
        self.kernel = Kernel(os.getcwd() + '/__main__.py')

    def test_command_line_args(self):
        self.assertTrue(
            self.kernel.validate_argv([True, True]),
        )

        self.assertFalse(
            self.kernel.validate_argv([True]),
        )
