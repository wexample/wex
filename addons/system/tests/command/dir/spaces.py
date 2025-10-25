from __future__ import annotations
from tests.AbstractTestCase import AbstractTestCase


class TestSystemCommandDirSpaces(AbstractTestCase):
    def test_spaces(self) -> None:
        from addons.system.command.dir.spaces import system__dir__spaces
        self.assertIsNotNone(self.kernel.run_function(system__dir__spaces))
