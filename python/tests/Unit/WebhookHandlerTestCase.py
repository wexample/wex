import unittest
from src.core.WebhookHandler import WebhookHandler
import os

class WebhookHandlerTestCase(unittest.TestCase):
    def test_simple(self):
        success = WebhookHandler(os.getcwd()).parse_url_and_execute(
            'http://localhost:4242/webhook/wex-test/test'
        )

        self.assertTrue(success)

    def test_args(self):
        success = WebhookHandler(os.getcwd()).parse_url_and_execute(
            'http://localhost:4242/webhook/wex-test/test?lorem=ipsum'
        )

        self.assertTrue(success)

    def test_values(self):
        success = WebhookHandler(os.getcwd()).parse_url_and_execute(
            'http://localhost:4242/webhook/wex-test/test-wraped?p=155&v=wex_5.0.0-beta.6+build.20230321054915'
        )

        self.assertTrue(success)
