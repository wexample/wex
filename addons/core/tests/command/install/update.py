from addons.core.command.install.update import core__install__update
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandInstallUpdate(AbstractTestCase):
    def test_update(self):
        response = self.kernel.run_function(
            core__install__update
        )

        self.assertTrue(
            # Test only update passed
            'Hit:1 ' in response.print(),
        )
