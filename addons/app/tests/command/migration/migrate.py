import os
from typing import List

from addons.app.command.migration.migrate import app__migration__migrate
from tests.AbstractTestCase import AbstractTestCase


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
            test_app_dir = self.build_test_dir(
                source_apps_dir + test_app_dir
            )

            self.kernel.run_function(
                app__migration__migrate, {
                    'app-dir': test_app_dir
                }
            )


