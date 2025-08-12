import os
import shutil

from wexample_helpers.helpers.file import file_remove_if_exists

from addons.core.command.command.create import core__command__create
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandCommandCreate(AbstractTestCase):
    def test_create(self) -> None:
        test_file_path_command = f"command/lorem/ipsum.py"
        test_file_path = (
            self.kernel.get_path("addons", ["core"]) + test_file_path_command
        )
        test_file_path_test = (
            self.kernel.get_path("addons", ["core", "tests"]) + test_file_path_command
        )

        file_remove_if_exists(test_file_path)
        file_remove_if_exists(test_file_path_test)

        self.kernel.run_function(
            core__command__create, {"command": "core::lorem/ipsum"}
        )

        self.assertPathExists(test_file_path)

        self.assertPathExists(test_file_path_test)

        # Cleanup created file.
        shutil.rmtree(os.path.dirname(test_file_path))

        shutil.rmtree(os.path.dirname(test_file_path_test))

    def test_create_local(self) -> None:
        self.kernel.run_function(core__command__create, {"command": "~test/create"})

    def test_create_dash(self) -> None:
        result = self.kernel.run_function(
            core__command__create, {"command": "core::test-with-dash/create"}
        ).first()

        shutil.rmtree(os.path.dirname(result["command"]))

        shutil.rmtree(os.path.dirname(result["test"]))
