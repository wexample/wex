
from AbstractTestCase import AbstractTestCase

from src.core.FatalError import FatalError
from src.helper.file import file_remove_file_if_exists


class TestLogging(AbstractTestCase):
    def test_error(self):
        file_remove_file_if_exists(self.kernel.get_or_create_path('task'))

        with self.assertRaises(FatalError, msg=None):
            self.kernel.io.error(
                message='ERR_TEST'
            )

        self.assertPathExists(
            self.kernel.get_or_create_path('task')
        )

    def test_history(self):
        file_remove_file_if_exists(self.kernel.get_or_create_path('task'))

        self.kernel.run_command('hi')

        self.kernel.logger.append_event(
            'EVENT_TEST',
            {
                'command': 'test-command',
                'success': True
            }
        )

        self.assertPathExists(
            self.kernel.get_or_create_path('task')
        )
