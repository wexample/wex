from AbstractTestCase import AbstractTestCase
from addons.core.command.webhook.exec import core__webhook__exec


class WebhookHandlerTestCase(AbstractTestCase):
    def test_simple(self):
        success = self.kernel.exec_function(
            core__webhook__exec,
            {
                'url': 'http://localhost:4242/webhook/wex/test'
            }
        )

        self.assertTrue(success)

    def test_args(self):
        success = self.kernel.exec_function(
            core__webhook__exec,
            {
                'url': 'http://localhost:4242/webhook/wex/test?lorem=ipsum'
            }
        )

        self.assertTrue(success)

    def test_values(self):
        success = self.kernel.exec_function(
            core__webhook__exec,
            {
                'url': 'http://localhost:4242/webhook/wex/test-wraped?p=155&v=wex_5.0.0-beta.6+build.20230321054915'
            }
        )

        self.assertTrue(success)
