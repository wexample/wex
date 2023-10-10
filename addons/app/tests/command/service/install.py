from addons.app.command.service.install import app__service__install
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandServiceInstall(AbstractAppTestCase):
    def test_install(self):
        app_dir = self.create_test_app()

        self.kernel.run_function(
            app__service__install, {
                'app-dir': app_dir,
                'service': 'nextcloud'
            }
        )

        self.stop_test_app()
