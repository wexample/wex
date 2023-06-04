import logging

from AbstractTestCase import AbstractTestCase
from src.helper.file import remove_file_if_exists
from src.const.error import ERR_TEST


class TestLogging(AbstractTestCase):
    def test_error(self):
        remove_file_if_exists(self.kernel.path['history'])

        self.kernel.error(
            code=ERR_TEST,
            log_level=logging.DEBUG
        )

        self.assertFileExists(
            self.kernel.path['history']
        )

    def test_history(self):
        remove_file_if_exists(self.kernel.path['history'])

        self.kernel.add_to_history(
            {
                'command': 'test-command',
                'success': True
            }
        )

        self.assertFileExists(
            self.kernel.path['history']
        )
