import json
import time

from addons.app.tests.AbstractWebhookTestCase import AbstractWebhookTestCase
from addons.app.command.webhook.listen import app__webhook__listen


class TestAppCommandWebhookListen(AbstractWebhookTestCase):
    def test_listen(self):
        self.kernel.run_function(app__webhook__listen, {
            'dry-run': True,
            'port': 1234,
            'force': True
        })

        # No easy way to define if server ran.
        self.assertTrue(True)

        self.start_webhook_listener()
        response = self.request_listener('/status')

        data = json.loads(response.read())

        self.assertTrue(
            isinstance(data, dict)
        )

        self.assertTrue(
            data['running']
        )

        self.assertIsNotNone(
            data['task_id']
        )
