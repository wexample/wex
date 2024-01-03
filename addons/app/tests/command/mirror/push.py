from src.helper.command import execute_command_sync
from tests.AbstractTestCase import AbstractTestCase
from addons.app.command.remote.available import app__remote__available


class TestAppCommandMirrorPush(AbstractTestCase):
    def test_push(self) -> None:
        response = self.kernel.run_function(
            app__remote__available, {
                "environment": "test-mirror",
                "app-dir": self.kernel.directory.path
            }
        )

        self.log('Starting fake test remote server')
        command = ["docker", "compose", "-f", ".wex/docker/docker-compose.test-remote.yml", "up", "-d"]

        execute_command_sync(
            self.kernel,
            command)

        self.log('Stopping fake test remote server')
        command = ["docker", "compose", "-f", ".wex/docker/docker-compose.test-remote.yml", "down"]

        execute_command_sync(
            self.kernel,
            command)

