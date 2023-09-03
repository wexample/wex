from addons.core.command.test_command.exec_thread import core__test_command__exec_thread
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandTestCommandExecThread(AbstractTestCase):
    def test_exec_thread(self):
        response = self.kernel.run_function(
            core__test_command__exec_thread
        )

        self.assertEqual(
            response,
            2
        )
