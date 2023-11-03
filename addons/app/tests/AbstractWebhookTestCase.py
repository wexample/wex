import time
import json

from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from addons.app.command.webhook.listen import app__webhook__listen
from http.client import HTTPConnection


class AbstractWebhookTestCase(AbstractAppTestCase):
    def start_webhook_listener(self, port: int = 6543):
        self.kernel.run_function(app__webhook__listen, {
            'port': port,
            'asynchronous': True,
            'force': True
        })

        time.sleep(2)

        return port

    def request_listener(self, path: str, port: int = 6543, check_code: None | int = 200):
        conn = HTTPConnection(f'localhost:{port}')
        conn.request("GET", path)
        response = conn.getresponse()

        if check_code:
            self.assertEqual(
                response.status,
                check_code
            )

        return response

    def parse_response(self, response) -> dict:
        return json.loads(response.read())
