from addons.app.command.webhook.status import app__webhook__status
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandWebhookStatus(AbstractTestCase):
    def test_status(self):
        response = self.kernel.run_function(app__webhook__status)
        data = response.first()

        self.assertTrue(
            'log' in data,
        )
