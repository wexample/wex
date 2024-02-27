import os.path
import time

from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.db.exec import app__db__exec
from addons.app.command.remote.exec import app__remote__exec
from addons.app.command.remote.push import app__remote__push
from addons.app.helper.remote import remote_build_temp_push_dir
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from src.helper.command import execute_command_sync
from src.const.types import StringsList


class TestAppCommandRemotePush(AbstractAppTestCase):
    def test_push(self) -> None:
        self._test_push_with_db()

    def _test_push_with_db(self) -> None:
        manager = self._prepare_sync_env(services=["php", "mysql"])

        app_dir = manager.get_app_dir()
        app_dir_basename = os.path.basename(os.path.dirname(app_dir))
        app_name = manager.get_app_name()
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

        from addons.app.helper.remote import (
            remote_get_connexion_address,
            remote_get_connexion_command,
        )

        address = remote_get_connexion_address(
            manager=manager, environment=environment, command=app__remote__exec
        )

        if not address:
            return None

        print(' '.join(
            remote_get_connexion_command(
                manager=manager, environment=environment
            )
            + [address],
        ))

        time.sleep(600)

        # Now than app has been updated,
        # we create a mirror in remote environment.
        self.create_remote_mirror(app_dir=app_dir, environment=environment)

        # Now that app has been mirrored, we add a data in database
        # it will test if database has been migrated as expected.
        unique_value = f"test_{int(time.time())}"

        self.kernel.run_function(
            app__db__exec,
            {
                "app-dir": app_dir,
                "command": f"CREATE TABLE IF NOT EXISTS "
                f"test_migration (id INT AUTO_INCREMENT PRIMARY KEY, test_value VARCHAR(255) NOT NULL); "
                f"INSERT INTO test_migration (test_value) VALUES ('{unique_value}');",
            },
        )

        self.kernel.run_function(
            app__remote__push, {"environment": environment, "app-dir": app_dir}
        )

        remote_temp_push_dir = remote_build_temp_push_dir(environment, app_name)

        response = self.kernel.run_function(
            app__remote__exec,
            {
                "app-dir": app_dir,
                "environment": environment,
                "command": f"ls -la {remote_temp_push_dir}test_subdir/subdir-file.txt",
            },
        )

        self.log(response.first())

        lines = response.first().split("\n")
        self.assertTrue(
            # The last line is the file info.
            lines[len(lines) - 1].startswith("-rw"),
            "The local file has been created remotely",
        )

        self.kernel.run_function(
            app__remote__exec,
            {
                "app-dir": app_dir,
                "environment": environment,
                "command": f"ls -la {remote_temp_push_dir}",
            },
        )

        response = self.kernel.run_function(
            app__remote__exec,
            {
                "app-dir": app_dir,
                "environment": environment,
                "command": f'cd /var/www/{environment}/{app_dir_basename} && wex db/exec -c "SELECT test_value FROM {app_name}.test_migration"',
            },
        )

        self.assertEqual(
            response.first().split("\n")[1],
            unique_value,
            "The value in the local database hase been transferred and mounted in remote database",
        )

    def _prepare_sync_env(self, services: StringsList) -> AppAddonManager:
        manager = self.create_and_start_test_app_with_remote(services)

        return manager
