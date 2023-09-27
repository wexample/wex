import os

from addons.core.command.logs.rotate import core__logs__rotate
from tests.AbstractTestCase import AbstractTestCase


def _change_modification_time(test_log_path, days):
    current_modification_time = os.path.getmtime(test_log_path)
    new_modification_time = current_modification_time - days * 24 * 60 * 60
    os.utime(test_log_path, (new_modification_time, new_modification_time))


class TestCoreCommandLogsRotate(AbstractTestCase):
    def test_rotate(self):
        test_log_path = os.path.join(self.kernel.path['log'], 'test.json')

        with open(test_log_path, 'w') as test_log:
            test_log.write('TEST_CONTENT')

        # File has been modified 10 days ago.
        _change_modification_time(
            test_log_path,
            1
        )

        self.kernel.run_function(core__logs__rotate)
        self.assertPathExists(test_log_path)

        # File has been modified 100 days ago.
        _change_modification_time(
            test_log_path,
            100
        )

        self.kernel.run_function(core__logs__rotate)
        self.assertPathExists(test_log_path, False)