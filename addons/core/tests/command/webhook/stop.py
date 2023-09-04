from addons.core.command.webhook.stop import core__webhook__stop
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandWebhookStop(AbstractTestCase):
    def test_stop(self):
        self.kernel.run_function(core__webhook__stop)
