import os
from typing import List

from addons.app.command.migration.migrate import app__migration__migrate
from src.helper.core import core_kernel_get_version
from src.const.globals import CORE_COMMAND_NAME
from tests.AbstractTestCase import AbstractTestCase
from addons.app.AppAddonManager import AppAddonManager


class TestAppCommandMigrationMigrate(AbstractTestCase):
    def test_migrate(self):
        source_apps_dir = os.path.join(
            self.kernel.path['root'],
            'tests',
            'resources',
            'app',
        ) + os.sep

        test_apps: List[str] = os.listdir(source_apps_dir)

        for test_app_dir in test_apps:
            self.log(f'Migrating test app {test_app_dir}')

            test_app_dir = self.build_test_dir(
                source_apps_dir + test_app_dir
            ) + os.sep

            self.kernel.run_function(
                app__migration__migrate, {
                    'app-dir': test_app_dir,
                    'yes': True
                }
            )

            manager = AppAddonManager(self.kernel, 'app-migration')
            manager.set_app_workdir(test_app_dir)

            self.assertEqual(
                manager.config[CORE_COMMAND_NAME]['version'],
                core_kernel_get_version(self.kernel)
            )
