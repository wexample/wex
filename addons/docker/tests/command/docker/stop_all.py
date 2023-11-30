from addons.docker.command.docker.stop_all import docker__docker__stop_all
from tests.AbstractTestCase import AbstractTestCase


class TestDockerCommandDockerStopAll(AbstractTestCase):
    def test_stop_all(self) -> None:
        # We can't execute as it may stop current container to run.
        self.assertIsNotNone(docker__docker__stop_all)
