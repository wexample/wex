from addons.docker.command.docker.ip import docker__docker__ip
from tests.AbstractTestCase import AbstractTestCase


class TestDockerCommandDockerIp(AbstractTestCase):
    def test_ip(self):
        self.assertIsNotNone(
            self.kernel.exec_function(docker__docker__ip)
        )