from addons.app.helpers.test import create_test_app
from addons.app.command.app.start import app__app__start
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandAppStart(AbstractTestCase):
    def test_start(self):
        app_dir = create_test_app(self.kernel, services=['php-8'])

        self.kernel.exec_function(
            app__app__start, {
                'app-dir': app_dir
            }
        )
