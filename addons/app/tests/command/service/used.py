from addons.app.command.service.install import app__service__install
from addons.app.command.service.used import app__service__used
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandServiceUsed(AbstractAppTestCase):
    def test_used(self):
        app_dir = self.create_test_app()

        self.kernel.run_function(
            app__service__install, {"app-dir": app_dir, "service": "nextcloud"}
        )

        self.assertTrue(
            self.kernel.run_function(
                app__service__used, {"app-dir": app_dir, "service": "nextcloud"}
            )
        )
