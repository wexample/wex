import os

from tests.AbstractTestCase import AbstractTestCase

from addons.core.command.webhook.exec import core__webhook__exec


class TestCoreCommandWebhookExec(AbstractTestCase):
    def test_exec(self):
        test_webhook_app_path = '/var/www/test/wex-test-webhook'
        if not os.path.islink(test_webhook_app_path):
            os.makedirs(
                os.path.dirname(test_webhook_app_path),
                exist_ok=True
            )
            os.symlink(
                self.kernel.get_path('root'),
                test_webhook_app_path
            )

        success = self.kernel.run_function(
            core__webhook__exec,
            {
                'url': 'http://localhost:4242/webhook/wex-test-webhook/test',
                'env': 'test'
            }
        ).first()

        self.assertTrue(success)

        success = self.kernel.run_function(
            core__webhook__exec,
            {
                'url': 'http://localhost:4242/webhook/wex-test-webhook/test?lorem=ipsum',
                'env': 'test'
            }
        ).first()

        self.assertTrue(success)

        success = self.kernel.run_function(
            core__webhook__exec,
            {
                'url': 'http://localhost:4242/webhook/wex-test-webhook/test-wrapped?p=155&v=wex_5.0.0-beta.6+build.20230321054915',
                'env': 'test'
            }
        ).first()

        self.assertTrue(success)
