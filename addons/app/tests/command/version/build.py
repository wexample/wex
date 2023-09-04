from addons.app.command.version.build import app__version__build
from addons.app.AppAddonManager import AppAddonManager
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandVersionBuild(AbstractTestCase):
    def test_build(self):
        manager: AppAddonManager = self.kernel.addons['app']
        current_version = manager.get_config('global.version')

        # Change version.
        version = self.kernel.run_function(
            app__version__build,
            {
                'version': '1.0.0'
            }
        )

        self.assertEqual(version, '1.0.0')

        # Rollback.
        self.kernel.run_function(
            app__version__build,
            {
                'version': current_version
            }
        )
