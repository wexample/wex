from __future__ import annotations
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandCoreUninstall(AbstractTestCase):
    def test_uninstall(self) -> None:
        from addons.core.command.core.uninstall import core__core__uninstall

        self.assertIsNotNone(core__core__uninstall)
