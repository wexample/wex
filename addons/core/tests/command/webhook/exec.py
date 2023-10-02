import os

from tests.AbstractTestCase import AbstractTestCase

from addons.core.command.webhook.exec import core__webhook__exec


class TestCoreCommandWebhookExec(AbstractTestCase):
    def test_exec(self):
        test_webhook_app_path = '/var/www/local/wex-test-webhook'
        if not os.path.exists(test_webhook_app_path):
            os.symlink(
                self.kernel.path['root'],
                test_webhook_app_path
            )

        success = self.kernel.run_function(
            core__webhook__exec,
            {
                'url': 'http://localhost:4242/webhook/wex-test-webhook/test'
            }
        ).first()

        self.assertTrue(success)

        success = self.kernel.run_function(
            core__webhook__exec,
            {
                'url': 'http://localhost:4242/webhook/wex-test-webhook/test?lorem=ipsum'
            }
        ).first()

        self.assertTrue(success)

        success = self.kernel.run_function(
            core__webhook__exec,
            {
                'url': 'http://localhost:4242/webhook/wex-test-webhook/test-wraped?p=155&v=wex_5.0.0-beta.6+build.20230321054915'
            }
        ).first()

        self.assertTrue(success)
