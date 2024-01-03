import os

from src.helper.command import execute_command_sync
from addons.app.command.mirror.push import app__mirror__push
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from addons.app.AppAddonManager import AppAddonManager


class TestAppCommandMirrorPush(AbstractAppTestCase):
    def test_push(self) -> None:
        app_dir = self.create_and_start_test_app(services=["php"])

        self.log('Starting fake test remote server')
        command = ["docker", "compose", "-f", ".wex/docker/docker-compose.test-remote.yml", "up", "-d", "--build"]

        environment = "test-remote"

        execute_command_sync(
            self.kernel,
            command)

        execute_command_sync(
            self.kernel,
            command)

        # Get IP
        command = ["docker", "inspect", "-f", "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}",
                   "wex_test_remote"]
        success, ip_list = execute_command_sync(
            self.kernel,
            command)

        ip: str = ip_list[0]

        # Reuse manager to work with
        manager = AppAddonManager(self.kernel, app_dir=app_dir)
        manager.set_config("env.test-remote.server.ip", ip)

        execute_command_sync(
            manager.kernel,
            ["touch", f"{app_dir}test.txt"])

        response = self.kernel.run_function(
            app__mirror__push, {
                "environment": "test-remote",
                "app-dir": app_dir
            }
        )

        remote_path = f"/var/www/{environment}/{manager.get_config('global.name').get_str()}/"
        command = ["sshpass", "-p", "TEST_PASSWORD", "ssh", "-o", "StrictHostKeyChecking=no", f"root@{ip}",
                   f"ls -la {remote_path}test.txt"]

        success, files_list = execute_command_sync(
            self.kernel,
            command)

        self.assertTrue(
            files_list[0].startswith('-rwxr-xr-x'),
            "The local file has been created remotely"
        )

        # Rollback to working dir.
        os.chdir(self.kernel.directory.path)

        self.log('Stopping fake test remote server')
        command = ["docker", "compose", "-f", ".wex/docker/docker-compose.test-remote.yml", "down", "--rmi", "all"]

        execute_command_sync(
            self.kernel,
            command)
