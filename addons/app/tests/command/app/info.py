from addons.app.command.app.info import app__app__info
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from addons.app.helpers.test import DEFAULT_APP_TEST_NAME


class TestAppCommandAppInfo(AbstractAppTestCase):
    def test_info(self):
        # No error in non app.
        response = self.kernel.run_function(app__app__info, {
            'app-dir': '/var/tmp'
        })

        self.assertIsNotNone(response.first())

        app_dir = self.create_test_app(
            DEFAULT_APP_TEST_NAME)

        self.kernel.run_function(app__app__info, {
            'app-dir': app_dir
        })

        self.assertIsNotNone(response.first())
