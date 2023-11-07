from addons.app.tests.AbstractWebhookTestCase import AbstractWebhookTestCase
from addons.app.WebhookHttpRequestHandler import WEBHOOK_STATUS_COMPLETE, WEBHOOK_STATUS_STARTED
from src.core.Logger import LOG_STATUS_COMPLETE
from src.const.globals import CORE_COMMAND_NAME
from addons.app.AppAddonManager import AppAddonManager
import time


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

        self.assertEqual(
            json['status'],
            WEBHOOK_STATUS_COMPLETE
        )

        # Async hook
        response = self.request_listener(
            '/webhook/wex/test-waiting',
            check_code=None
        )

        json = self.parse_response(response)

        self.assertEqual(
            json['status'],
            'started'
        )

        self.assertIsNotNone(
            json['task_id'],
        )

        task_id = json['task_id']

        self.log('Waiting task to terminate : ' + task_id)
        time.sleep(2)

        response = self.request_listener(
            f'/status/process/{task_id}',
        )

        json = self.parse_response(response)

        self.assertEqual(
            json['task_id'],
            task_id
        )

        self.assertEqual(
            json['status'],
            LOG_STATUS_COMPLETE
        )
