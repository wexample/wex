from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.remote.exec import app__remote__exec
from addons.app.command.remote.push import app__remote__push
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from src.const.types import StringsList


class TestAppCommandRemotePush(AbstractAppTestCase):
    def test_push(self) -> None:
        self._test_push_with_db()

    def _test_push_with_db(self) -> None:
        manager = self._prepare_sync_env(services=["php", "mysql"])

        app_dir = manager.get_app_dir()
        test_filename = "structure-test.txt"

        manager.set_config(
            key=["structure", "schema", test_filename],
            value={
                "type": "file",
                "should_exist": True,
                "on_missing": "create",
                "default_content": "This is a test file created by structure manager.",
                "remote": "push",
            },
        )

        manager.set_config(
            key=f"structure.schema.test_subdir",
            value={
                # should_exist:True + on_missing:create + remote:push
                # are implicit as it was set on a child file.
                "type": "dir",
                "schema": {
                    "subdir-file.txt": {
                        "type": "file",
                        "should_exist": True,
                        "on_missing": "create",
                        "default_content": "This is a file placed in a subdirectory "
                        "which should also be push to remote server.",
                        "remote": "push",
                    }
                },
            },
        )

        self.reload_app_manager()

        environment = "test_remote"

        self.kernel.run_function(
            app__remote__push, {"environment": environment, "app-dir": app_dir}
        )

        response = self.kernel.run_function(
            app__remote__exec,
            {
                "app-dir": app_dir,
                "environment": environment,
                "command": f"ls -la ~/pushed/{environment}/{manager.get_app_name()}/test_subdir/subdir-file.txt",
            },
        )

        self.log(response.first())

        lines = response.first().split("\n")
        self.assertTrue(
            # The last line is the file info.
            lines[len(lines) - 1].startswith("-rw"),
            "The local file has been created remotely",
        )

        response = self.kernel.run_function(
            app__remote__exec,
            {
                "app-dir": app_dir,
                "environment": environment,
                "command": f"ls -la ~/pushed/{environment}/{manager.get_app_name()}",
            },
        )

        self.log(response.first())

    def _prepare_sync_env(self, services: StringsList) -> AppAddonManager:
        manager = self.create_and_start_test_app_with_remote(services)

        return manager
