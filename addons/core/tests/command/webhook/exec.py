from tests.AbstractTestCase import AbstractTestCase

from addons.core.command.webhook.exec import core__webhook__exec


class TestCoreCommandWebhookExec(AbstractTestCase):
    def test_exec(self):
        success = self.kernel.exec_function(
            core__webhook__exec,
            {
                'url': 'http://localhost:4242/webhook/wex/test'
            }
        )

        self.assertTrue(success)

        success = self.kernel.exec_function(
            core__webhook__exec,
            {
                'url': 'http://localhost:4242/webhook/wex/test?lorem=ipsum'
            }
        )

        self.assertTrue(success)

        success = self.kernel.exec_function(
            core__webhook__exec,
            {
                'url': 'http://localhost:4242/webhook/wex/test-wraped?p=155&v=wex_5.0.0-beta.6+build.20230321054915'
            }
        )

        self.assertTrue(success)
