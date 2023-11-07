from addons.app.tests.AbstractWebhookTestCase import AbstractWebhookTestCase
from addons.app.WebhookHttpRequestHandler import WEBHOOK_STATUS_COMPLETE, WEBHOOK_STATUS_STARTED
from src.const.globals import CORE_COMMAND_NAME
from addons.app.AppAddonManager import AppAddonManager


class TestAppCommandWebhookExec(AbstractWebhookTestCase):
    def test_exec(self):
        manager = AppAddonManager(
            self.kernel,
            app_dir=self.kernel.path['root']
        )

        # Add application as a local app
        manager.add_proxy_app(
            CORE_COMMAND_NAME,
            app_dir=self.kernel.path['root']
        )

        self.start_webhook_listener()

        # Check status
        response = self.request_listener(
            '/status',
        )

        json = self.parse_response(response)

        self.assertEqual(
            json['status'],
            WEBHOOK_STATUS_COMPLETE
        )

        # Missing hook
        response = self.request_listener(
            '/webhook/wex/missing-hook',
        )

        json = self.parse_response(response)

        # Even missing, returns okay as it is an async response.
        self.assertEqual(
            json['status'],
            WEBHOOK_STATUS_STARTED
        )

        response = self.request_listener(
            f'/status/process/{json["task_id"]}',
        )

        json = self.parse_response(response)
