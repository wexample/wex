from addons.app.helpers.test import create_test_app
from addons.app.command.config.get import app__config__get
from tests.AbstractTestCase import AbstractTestCase

from addons.app.command.config.set import app__config__set


class TestAppCommandConfigSet(AbstractTestCase):
    def test_set(self):
        app_dir = create_test_app(self.kernel)

        # Change value.
        self.kernel.run_function(app__config__set, {
            'app-dir': app_dir,
            'key': 'global.name',
            'value': 'wex-test-config-set'
        })

        self.assertEqual(self.kernel.run_function(
            app__config__get,
            {
                'app-dir': app_dir,
                'key': 'global.name'
            }
        ), 'wex-test-config-set')

        # Rollback.
        self.kernel.run_function(app__config__set, {
            'app-dir': app_dir,
            'key': 'global.name',
            'value': 'wex'
        })

        self.assertEqual(self.kernel.run_function(
            app__config__get,
            {
                'app-dir': app_dir,
                'key': 'global.name'
            }
        ), 'wex')
