from addons.app.command.app.start import app__app__start
from addons.app.command.config.write import app__config__write
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandConfigWrite(AbstractAppTestCase):
    def test_write(self):
        app_dir = self.create_test_app(
            services=['php'],
            force_restart=True)

        self.kernel.run_function(
            app__config__write, {
                'app-dir': app_dir
            }
        )

        self.kernel.run_function(
            app__app__start, {
                'app-dir': app_dir
            }
        )

        self.kernel.run_function(
            app__config__write, {
                'app-dir': app_dir
            }
        )
