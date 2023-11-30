import json
import os

from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.app.exec import app__app__exec
from addons.app.command.webhook.exec import app__webhook__exec
from addons.app.tests.AbstractWebhookTestCase import AbstractWebhookTestCase
from addons.app.WebhookHttpRequestHandler import (
    WEBHOOK_STATUS_COMPLETE,
    WEBHOOK_STATUS_STARTED,
)
from src.const.globals import CORE_COMMAND_NAME
from src.core.Logger import LOG_STATUS_COMPLETE


class TestAppCommandWebhookExec(AbstractWebhookTestCase):
    def test_exec(self) -> None:
        manager = AppAddonManager(self.kernel, app_dir=self.kernel.path["root"])

        # Add application as a local app
        manager.add_proxy_app(CORE_COMMAND_NAME, app_dir=self.kernel.path["root"])

        self.start_webhook_listener()

        # Check status
        http_response = self.request_listener(
            "/status",
        )

        data = self.parse_response(http_response)

        self.assertEqual(data["status"], WEBHOOK_STATUS_COMPLETE)

        # Missing hook
        http_response = self.request_listener(
            "/webhook/wex/missing-hook",
        )

        data = self.parse_response(http_response)

        # Even missing, returns okay as it is an async response.
        self.assertEqual(data["status"], WEBHOOK_STATUS_STARTED)

        http_response = self.request_listener(
            f'/status/process/{data["task_id"]}',
        )

        data = self.parse_response(http_response)

        self.assertEqual(data["status"], WEBHOOK_STATUS_COMPLETE)

        # Async hook
        http_response = self.request_listener(
            "/webhook/app/wex/webhook/test-waiting", check_code=None, wait=2
        )

        data = self.parse_response(http_response)

        self.assertEqual(data["status"], "started")

        self.assertIsNotNone(
            data["task_id"],
        )

        task_id = data["task_id"]

        http_response = self.request_listener(
            f"/status/process/{task_id}",
        )

        data = self.parse_response(http_response)

        self.assertEqual(data["task_id"], task_id)

        self.assertEqual(data["status"], LOG_STATUS_COMPLETE)

        app_dir, app_name = self.create_and_start_test_app_webhook()

        self.kernel.run_function(
            app__app__exec, {"app-dir": app_dir, "command": "touch /var/tmp/test-file"}
        )

        response = self.kernel.run_function(
            app__webhook__exec,
            {
                "webhook_path": f"/webhook/app/{app_name}/test/test-running",
            },
        )

        data = json.loads(str(response.print_wrapped(render_mode="json")))

        lines = data["value"].split(os.linesep)

        self.assertEqual(lines[0], "BASH_RESPONSE_RUNNING")

        self.assertTrue(" test-file" in lines[4])

        self.assertEqual(lines[5], "TEST_EXECUTION_ORDER")

        self.stop_test_app(app_dir)
