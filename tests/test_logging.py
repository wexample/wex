import logging

from AbstractTestCase import AbstractTestCase
from src.helper.file import remove_file_if_exists
from src.const.error import ERR_TEST


class TestLogging(AbstractTestCase):
    def test_error(self):
        remove_file_if_exists(self.kernel.path['log'])

        self.kernel.io.error(
            code=ERR_TEST,
            log_level=logging.DEBUG
        )

        self.assertPathExists(
            self.kernel.path['log']
        )

    def test_history(self):
        remove_file_if_exists(self.kernel.path['log'])

        self.kernel.run_command('hi')

        self.kernel.logger.append_event(
            {
                'command': 'test-command',
                'success': True
            }
        )

        self.assertPathExists(
            self.kernel.path['log']
        )
