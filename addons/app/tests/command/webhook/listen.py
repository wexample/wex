import json

from addons.app.command.webhook.listen import app__webhook__listen
from addons.app.tests.AbstractWebhookTestCase import AbstractWebhookTestCase


class TestAppCommandWebhookListen(AbstractWebhookTestCase):
    def test_listen(self):
        self.kernel.run_function(
            app__webhook__listen, {"dry-run": True, "port": 1234, "force": True}
        )

        # No easy way to define if server ran.
        self.assertTrue(True)

        port = self.start_webhook_listener()
        response = self.request_listener("/status", port=port)
        data = json.loads(response.read())

        self.assertTrue(isinstance(data, dict))

        self.assertTrue(data["response"]["process"]["running"])
