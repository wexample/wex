from addons.app.command.app.started import app__app__started
from addons.app.helpers.test import create_test_app
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandAppStarted(AbstractTestCase):
    def test_started(self):
        app_dir = create_test_app(self.kernel, services=['php_8'])

        result = self.kernel.run_function(
            app__app__started,
            {
                'app-dir': app_dir,
            }
        )

        self.assertFalse(result)
