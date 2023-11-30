from addons.app.command.webhook.status import app__webhook__status
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandWebhookStatus(AbstractTestCase):
    def test_status(self) -> None:
        response = self.kernel.run_function(app__webhook__status)

        self.assertResponseFirstContains(
            response,
            "process")
