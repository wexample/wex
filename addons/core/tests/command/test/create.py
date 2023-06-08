import os
import shutil

from addons.core.command.test.create import core__test__create
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandTestCreate(AbstractTestCase):
    def test_create(self):
        test_file_path_command = f'command/lorem/ipsum.py'
        test_file_path_test = f"{self.kernel.path['addons']}core/tests/{test_file_path_command}"

        self.kernel.exec_function(
            core__test__create,
            {
                'command': 'core::lorem/ipsum'
            }
        )

        self.assertPathExists(
            test_file_path_test
        )

        shutil.rmtree(
            os.path.dirname(
                test_file_path_test
            )
        )
