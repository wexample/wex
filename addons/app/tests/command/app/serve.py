from addons.app.command.app.serve import app__app__serve
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandAppServe(AbstractAppTestCase):
    def test_serve(self):
        app_dir = self.create_and_start_test_app(services=['php'])

        self.kernel.run_function(
            app__app__serve, {
                'app-dir': app_dir
            }
        )

        self.stop_test_app()
