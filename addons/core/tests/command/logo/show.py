from addons.core.command.logo.show import core__logo__show
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandLogoShow(AbstractTestCase):
    def test_show(self):
        logo = self.kernel.exec_function(core__logo__show)

        self.assertTrue(
            'wexample' in logo
        )
