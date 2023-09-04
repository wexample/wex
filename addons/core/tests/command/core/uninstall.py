from addons.core.command.core.uninstall import core__core__uninstall
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandCoreUninstall(AbstractTestCase):
    def test_uninstall(self):
        self.assertIsNotNone(
            core__core__uninstall
        )
