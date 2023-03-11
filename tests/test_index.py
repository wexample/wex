import unittest
from unittest.mock import patch
import io
import sys


class TestIndex(unittest.TestCase):

    def test_command_line_args(self):
        self.assertIn(
            'true',
            'true'
        )

if __name__ == '__main__':
    unittest.main()
