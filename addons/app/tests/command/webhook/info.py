from addons.system.tests.command.process.by_port import TestSystemCommandProcessByPort
from src.const.globals import WEBHOOK_LISTEN_PORT_DEFAULT
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandWebhookInfo(AbstractTestCase):
    def test_info(self) -> None:
        test = TestSystemCommandProcessByPort()
        test.kernel = self.kernel

        test.test_by_port(port=WEBHOOK_LISTEN_PORT_DEFAULT)
