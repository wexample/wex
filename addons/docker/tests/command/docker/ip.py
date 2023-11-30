from addons.docker.command.docker.ip import docker__docker__ip
from tests.AbstractTestCase import AbstractTestCase


class TestDockerCommandDockerIp(AbstractTestCase):
    def test_ip(self) -> None:
        self.assertIsNotNone(self.kernel.run_function(docker__docker__ip))
