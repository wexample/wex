from __future__ import annotations
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandCoreInstall(AbstractTestCase):
    def test_install(self) -> None:
        from addons.core.command.core.install import core__core__install

        self.kernel.run_function(core__core__install)
