from addons.app.command.notification.notify import app__notification__notify
from addons.app.tests.AbstractWebhookTestCase import AbstractWebhookTestCase


class TestAppCommandNotificationNotify(AbstractWebhookTestCase):
    def test_notify(self) -> None:
        app_dir, app_name = self.create_and_start_test_app_webhook()

        response = self.kernel.run_function(
            app__notification__notify, {"action": "test"}
        )

        self.assertIsNone(response.print())
