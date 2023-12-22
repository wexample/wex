import json

from addons.app.tests.AbstractWebhookTestCase import AbstractWebhookTestCase
from src.helper.file import file_read


class TestTestCommandAppWebhook(AbstractWebhookTestCase):
    def test_webhook(self) -> None:
        response = self.kernel.run_command(
            # This is a yaml command.
            "test::app/webhook",
            {
                "option": "WEBHOOK_TEST_RESPONSE",
            },
        )

        self.assertResponseOutputBagItemContains(response, 4, "WEBHOOK_TEST_RESPONSE")

        app_dir, app_name = self.create_and_start_test_app_webhook()

        self.start_webhook_listener()

        http_response = self.request_listener(
            f"/webhook/app/{app_name}/test/test", check_code=None, wait=5
        )

        data = self.parse_response(http_response)
        listener_task_id = data["task_id"]

        log_stderr: str = self.kernel.task_file_path(
            "webhook-stderr", task_id=listener_task_id
        )
        log_stdout: str = self.kernel.task_file_path(
            "webhook-stdout", task_id=listener_task_id
        )

        stderr = file_read(log_stderr)
        if stderr:
            self.kernel.io.error(
                stderr
            )

        data = json.loads(file_read(log_stdout))

        lines = data["value"][0]

        self.assertEqual(stderr, "")

        self.assertEqual(lines[0][0], "MINIMAL_BASH_RESPONSE")

        self.assertEqual(lines[1][0], "BASH_RESPONSE")

        self.assertEqual(lines[2][0], "BASH_RESPONSE_FROM_FILE")

        self.assertEqual(lines[3][0], "PYTHON_SUCCESS")

        self.assertEqual(lines[4][0], "PYTHON_SUCCESS_FROM_FILE")
