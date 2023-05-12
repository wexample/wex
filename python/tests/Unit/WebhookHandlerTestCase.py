import unittest
from src.core.WebhookHandler import WebhookHandler
import os

class WebhookHandlerTestCase(unittest.TestCase):
    def test_simple(self):
        success = WebhookHandler(os.getcwd()).parse_url_and_execute(
            'http://localhost:4242/webhook/wex-test/test'
        )

        self.assertTrue(success)
