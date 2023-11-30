from addons.app.command.webhook.stop import app__webhook__stop
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandWebhookStop(AbstractTestCase):
    def test_stop(self) -> None:
        self.kernel.run_function(app__webhook__stop)
