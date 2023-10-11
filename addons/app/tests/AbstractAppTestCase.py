from tests.AbstractTestCase import AbstractTestCase
from addons.app.helpers.test import create_test_app, create_test_app_dir
from addons.app.command.app.start import app__app__start
from addons.app.command.app.stop import app__app__stop


class AbstractAppTestCase(AbstractTestCase):
    def create_test_app(self, name: str | None = None, services: list | None = None) -> str:
        return create_test_app(
            self.kernel,
            name=name,
            services=services or [],
        )

    def start_test_app(self, name: str | None = None):
        response = self.kernel.run_function(
            app__app__start, {
                'app-dir': create_test_app_dir(self.kernel, name)
            }
        )

        shell_response = response.output_bag[-2].first()

        self.log(shell_response)

        self.assertTrue(
            shell_response.find('Started') > 0,
        )

    def create_and_start_test_app(self, name: str | None = None, services: list | None = None) -> str:
        self.stop_test_app()

        app_dir = self.create_test_app(
            services=services,
        )

        self.start_test_app(name)

        return app_dir

    def stop_test_app(self, app_name: str | None = None):
        self.kernel.run_function(
            app__app__stop, {
                'app-dir': create_test_app_dir(self.kernel, app_name)
            }
        )
