from __future__ import annotations
from tests.AbstractTestCase import AbstractTestCase


class TestDockerCommandDockerIp(AbstractTestCase):
    def test_ip(self) -> None:
        from addons.docker.command.docker.ip import docker__docker__ip

        self.assertIsNotNone(self.kernel.run_function(docker__docker__ip))
