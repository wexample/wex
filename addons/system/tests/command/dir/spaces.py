from addons.system.command.dir.spaces import system__dir__spaces
from tests.AbstractTestCase import AbstractTestCase


class TestSystemCommandDirSpaces(AbstractTestCase):
    def test_spaces(self):
        self.assertIsNotNone(
            self.kernel.exec_function(system__dir__spaces)
        )
