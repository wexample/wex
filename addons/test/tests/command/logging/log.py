from addons.test.command.logging.log import test__logging__log
from src.const.globals import COMMAND_TYPE_ADDON
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandLoggingLog(AbstractTestCase):
    def test_log(self):
        response = self.kernel.run_function(
            test__logging__log
        )

        data = response.first()
        internal_command = self.kernel.get_command_resolver(COMMAND_TYPE_ADDON).build_command_from_function(
            test__logging__log)

        self.assertEqual(
            data['trace'][-1]['command'],
            internal_command
        )
