from addons.app.command.webhook.status_process import app__webhook__status_process
from src.const.globals import KERNEL_RENDER_MODE_JSON
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandWebhookStatusProcess(AbstractTestCase):
    def test_status_process(self):
        response = self.kernel.run_function(
            app__webhook__status_process, {"path": "/status/process/1234"}
        )

        self.assertEqual(response.first(), {})

        self.assertEqual(response.print(), "")

        response = self.kernel.run_function(
            app__webhook__status_process,
            {"path": "/status/process/1234"},
            render_mode=KERNEL_RENDER_MODE_JSON,
        )

        self.assertEqual(response.print(KERNEL_RENDER_MODE_JSON), {})
