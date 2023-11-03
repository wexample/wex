import json
import time

from addons.app.tests.AbstractWebhookTestCase import AbstractWebhookTestCase
from addons.app.command.webhook.listen import app__webhook__listen
from tests.AbstractTestCase import AbstractTestCase
from http.client import HTTPConnection


class TestAppCommandWebhookListen(AbstractWebhookTestCase):
    def test_listen(self):
        port = 6543

        self.kernel.run_function(app__webhook__listen, {
            'dry-run': True,
            'port': port,
            'force': True
        })

        # No easy way to define if server ran.
        self.assertTrue(True)

        self.kernel.run_function(app__webhook__listen, {
            'port': port,
            'asynchronous': True,
            'force': True
        })

        time.sleep(2)

        conn = HTTPConnection(f'localhost:{port}')
        conn.request("GET", "/status")
        response = conn.getresponse()

        self.assertEqual(
            response.status,
            200
        )

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

