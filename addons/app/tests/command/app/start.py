from addons.app.command.app.start import app__app__start
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandAppStart(AbstractAppTestCase):
    def test_start(self):
        app_dir = self.create_and_start_test_app(services=['php'])

        self.kernel.run_function(
            app__app__start, {
                'app-dir': app_dir
            }
        )
