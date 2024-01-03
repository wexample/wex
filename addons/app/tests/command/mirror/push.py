from src.helper.command import execute_command_sync
from tests.AbstractTestCase import AbstractTestCase
from addons.app.command.remote.available import app__remote__available


class TestAppCommandMirrorPush(AbstractTestCase):
    def test_push(self) -> None:
        response = self.kernel.run_function(
            app__remote__available, {
                "environment": "missing"}
        )

        self.assertEqual(response.first(), False)

        self.log('Starting fake test remote server')
        command = ["docker", "compose", "-f", ".wex/docker/docker-compose.test-remote.yml", "up", "-d", "--build"]

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

        self.log(f'Send test file to {ip}')
        command = ["sshpass", "-p", "TEST_PASSWORD", "scp", "-o", "StrictHostKeyChecking=no", f"{self.kernel.directory.path}version.txt", f"root@{ip}:/var/version.txt"]


        execute_command_sync(
            self.kernel,
            command)

        self.log('Stopping fake test remote server')
        command = ["docker", "compose", "-f", ".wex/docker/docker-compose.test-remote.yml", "down", "--rmi", "all"]

        execute_command_sync(
            self.kernel,
            command)
