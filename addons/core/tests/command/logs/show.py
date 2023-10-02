from addons.core.command.logs.show import core__logs__show
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandLogsShow(AbstractTestCase):
    def test_show(self):
        output = self.kernel.run_function(core__logs__show).first()

        self.assertTrue(
            len(output.splitlines()) > 0,
            "Output is empty or doesn't contain any lines."
        )
