from __future__ import annotations
from tests.AbstractTestCase import AbstractTestCase


class TestSystemCommandSystemIp(AbstractTestCase):
    def test_ip(self) -> None:
        from addons.system.command.system.ip import system__system__ip
        self.assertIsNotNone(self.kernel.run_function(system__system__ip))
