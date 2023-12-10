import os
from typing import List

from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.migration.migrate import app__migration__migrate
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from src.const.globals import CORE_COMMAND_NAME
from src.helper.core import core_kernel_get_version
from src.helper.dir import dir_execute_in_workdir


class TestAppCommandMigrationMigrate(AbstractAppTestCase):
    def test_migrate(self) -> None:
        source_apps_dir = self.get_app_resources_path()

        test_apps: List[str] = os.listdir(source_apps_dir)

        for test_app_dir in test_apps:
            self.log(f"Migrating test app {test_app_dir}")

            test_app_dir = self.build_test_dir(source_apps_dir + test_app_dir) + os.sep

            def _test_migrate() -> None:
                self.kernel.run_function(app__migration__migrate, {"yes": True})

                manager = AppAddonManager(self.kernel, app_dir=test_app_dir)

                self.assertEqual(
                    manager.get_config(f"{CORE_COMMAND_NAME}.version").get_str(),
                    core_kernel_get_version(self.kernel),
                )

            dir_execute_in_workdir(test_app_dir, _test_migrate)
