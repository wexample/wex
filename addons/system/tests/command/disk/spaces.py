from addons.system.command.disk.spaces import system__disk__spaces
from tests.AbstractTestCase import AbstractTestCase


class TestSystemCommandDiskSpaces(AbstractTestCase):
    def test_spaces(self):
        text = self.kernel.run_function(system__disk__spaces).first()

        self.assertIsNotNone(
            text
        )
