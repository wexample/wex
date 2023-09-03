from addons.app.helpers.test import create_test_app
from addons.app.command.service.install import app__service__install
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandServiceInstall(AbstractTestCase):
    def test_install(self):
        app_dir = create_test_app(self.kernel)

        self.kernel.run_function(
            app__service__install, {
                'app-dir': app_dir,
                'service': 'nextcloud'
            }
        )
