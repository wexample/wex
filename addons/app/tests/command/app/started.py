from addons.app.command.app.started import app__app__started
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandAppStarted(AbstractAppTestCase):
    def test_started(self) -> None:
        app_dir = self.create_and_start_test_app(services=["php"])

        result = self.kernel.run_function(
            app__app__started,
            {
                "app-dir": app_dir,
            },
        ).first()

        self.assertTrue(result)
