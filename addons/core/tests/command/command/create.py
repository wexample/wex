import os
import shutil

from addons.core.command.command.create import core__command__create
from src.helper.file import remove_file_if_exists
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandCommandCreate(AbstractTestCase):
    def test_create(self):
        test_file_path_command = f'command/lorem/ipsum.py'
        test_file_path = f"{self.kernel.path['addons']}core/{test_file_path_command}"
        test_file_path_test = f"{self.kernel.path['addons']}core/tests/{test_file_path_command}"

        remove_file_if_exists(test_file_path)
        remove_file_if_exists(test_file_path_test)

        self.kernel.exec_function(
            core__command__create,
            {
                'command': 'core::lorem/ipsum'
            }
        )

        self.assertPathExists(
            test_file_path
        )

        self.assertPathExists(
            test_file_path_test
        )

        # Cleanup created file.
        shutil.rmtree(
            os.path.dirname(
                test_file_path
            )
        )

        shutil.rmtree(
            os.path.dirname(
                test_file_path_test
            )
        )

    def test_create_local(self):
        self.kernel.exec_function(
            core__command__create,
            {
                'command': '~test/create'
            }
        )