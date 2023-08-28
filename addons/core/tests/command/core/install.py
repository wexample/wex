from addons.core.command.core.install import core__core__install
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandCoreInstall(AbstractTestCase):
    def test_install(self):
        self.kernel.exec_function(core__core__install)
