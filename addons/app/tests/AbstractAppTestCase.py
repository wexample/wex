from tests.AbstractTestCase import AbstractTestCase
from addons.app.helpers.test import create_test_app
from addons.app.command.app.start import app__app__start


class AbstractAppTestCase(AbstractTestCase):
    def create_and_start_text_app(self, services: list = []) -> str:
        app_dir = create_test_app(
            self.kernel,
            services=services,
        )

        response = self.kernel.run_function(
            app__app__start, {
                'app-dir': app_dir
            }
        )

        shell_message, success = response.output_bag[-2].output_bag

        self.assertTrue(
            success,
            shell_message
        )

        return app_dir
