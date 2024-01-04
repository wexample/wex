import os

from src.helper.command import execute_command_sync
from addons.app.command.remote.push import app__remote__push
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from addons.app.command.remote.exec import app__remote__exec


class TestAppCommandRemotePush(AbstractAppTestCase):
    def start_remote_server(self) -> None:
        self.log('Starting fake test remote server')
        command = ["docker", "compose", "-f", ".wex/docker/docker-compose.test-remote.yml", "up", "-d", "--build"]

        execute_command_sync(
            self.kernel,
            command)

    def stop_remote_server(self) -> None:
        # Rollback to working dir.
        os.chdir(self.kernel.directory.path)

        self.log('Stopping fake test remote server')
        command = ["docker", "compose", "-f", ".wex/docker/docker-compose.test-remote.yml", "down", "--rmi", "all"]

        execute_command_sync(
            self.kernel,
            command)

    def test_push(self) -> None:
        self.start_remote_server()

        manager = self.create_and_start_test_app_with_remote(services=["php"])
        app_dir = manager.get_app_dir()
        test_filename = "structure-test.txt"

        manager.set_config("structure", {
            test_filename: {
                "type": "file",
                "should_exist": True,
                "on_missing": "create",
                "default_content": "This is a test file created by structure manager",
                "remote": "push"
            },
        })

        # Reload updated config
        manager._directory.initialize()
        environment = "test-remote"

        execute_command_sync(
            manager.kernel,
            ["touch", f"{app_dir}test.txt"])

        self.kernel.run_function(
            app__remote__push, {
                "environment": "test-remote",
                "app-dir": app_dir
            }
        )

        remote_path = f"/var/www/{environment}/{manager.get_config('global.name').get_str()}/"

        response = manager.kernel.run_function(
            app__remote__exec,
            {
                "app-dir": app_dir,
                "environment": environment,
                "command": f"ls -la {remote_path}{test_filename}"
            }
        )

        self.assertTrue(
            response.first().startswith('-rwxr-xr-x'),
            "The local file has been created remotely"
        )

        self.stop_remote_server()
