from __future__ import annotations
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandVersionGet(AbstractTestCase):
    def test_get(self) -> None:
        from addons.core.command.version.get import core__version__get

        self.assertIsNotNone(self.kernel.run_function(core__version__get))
