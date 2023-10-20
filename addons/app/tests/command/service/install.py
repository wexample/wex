from addons.app.command.service.install import app__service__install
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from addons.app.command.config.write import app__config__write
from addons.app.helpers.test import DEFAULT_APP_TEST_NAME
from src.helper.registry import get_all_services_names


class TestAppCommandServiceInstall(AbstractAppTestCase):
    def test_install(self):
        services = get_all_services_names(self.kernel)

        for service in services:
            if service not in ['default', 'proxy']:
                self.log(f'Testing service install {service}')
                app_dir = self.create_test_app(
                    DEFAULT_APP_TEST_NAME + '-install-service',
                    force_restart=True)

                self.kernel.run_function(
                    app__service__install, {
                        'app-dir': app_dir,
                        'service': service
                    }
                )

                self.kernel.run_function(
                    app__config__write, {
                        'app-dir': app_dir
                    }
                )
