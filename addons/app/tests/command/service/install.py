import os

from addons.app.command.config.write import app__config__write
from addons.app.command.service.install import app__service__install
from addons.app.helper.test import DEFAULT_APP_TEST_NAME
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from src.const.globals import COMMAND_TYPE_SERVICE
from src.core.command.resolver.ServiceCommandResolver import ServiceCommandResolver


class TestAppCommandServiceInstall(AbstractAppTestCase):
    def test_install(self) -> None:
        resolver = self.kernel.resolvers[COMMAND_TYPE_SERVICE]
        assert isinstance(resolver, ServiceCommandResolver)
        services = resolver.get_registered_services()

        for service in services:
            if service not in ["default", "proxy"]:
                self.log(f"Testing service install {service}")
                os.chdir(self.kernel.get_path("call"))

                app_dir = self.create_test_app(
                    DEFAULT_APP_TEST_NAME + "-install-service", force_restart=True
                )

                self.kernel.run_function(
                    app__service__install, {"app-dir": app_dir, "service": service}
                )

                self.kernel.run_function(app__config__write, {"app-dir": app_dir})
