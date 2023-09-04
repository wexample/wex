from addons.system.command.system.ip import system__system__ip
from tests.AbstractTestCase import AbstractTestCase


class TestSystemCommandSystemIp(AbstractTestCase):
    def test_ip(self):
        self.assertIsNotNone(
            self.kernel.run_function(system__system__ip)
        )
