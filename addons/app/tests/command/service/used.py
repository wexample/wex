from addons.app.command.service.used import app__service__used
from addons.app.helpers.test import create_test_app
from addons.app.command.service.install import app__service__install
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandServiceUsed(AbstractTestCase):
    def test_used(self):
        app_dir = create_test_app(self.kernel)

        self.kernel.exec_function(
            app__service__install, {
                'app-dir': app_dir,
                'service': 'nextcloud'
            }
        )

        self.assertTrue(
            self.kernel.exec_function(
                app__service__used, {
                    'app-dir': app_dir,
                    'service': 'nextcloud'
                }
            )
        )
