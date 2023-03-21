import os

from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandLogsRotate(AbstractTestCase):
    def change_modification_time(self, test_log_path, days):
        current_modification_time = os.path.getmtime(test_log_path)
        new_modification_time = current_modification_time - days * 24 * 60 * 60
        os.utime(test_log_path, (new_modification_time, new_modification_time))

    def test_rotate(self):
        test_log_path = os.path.join(self.kernel.path['logs'], 'test.log')
        with open(test_log_path, 'w') as test_log:
            test_log.write('TEST_CONTENT')

        # File has been modified 10 days ago.
        self.change_modification_time(
            test_log_path,
            10
        )

        self.kernel.exec('core::logs/rotate')
        self.assertFileExists(test_log_path)

        # File has been modified 100 days ago.
        self.change_modification_time(
            test_log_path,
            100
        )

        self.kernel.exec('core::logs/rotate')
        self.assertFileExists(test_log_path, False)
