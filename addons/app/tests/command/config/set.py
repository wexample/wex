from tests.AbstractTestCase import AbstractTestCase

from addons.app.command.config.set import app__config__set
from addons.app.command.config.get import app__config__get


class TestAppCommandConfigSet(AbstractTestCase):
    def test_set(self):
        # Change value.
        self.kernel.exec_function(app__config__set, {
            'key': 'global.name',
            'value': 'wex-test-config-set'
        })

        self.assertEqual(self.kernel.exec_function(
            app__config__get,
            {
                'key': 'global.name'
            }
        ), 'wex-test-config-set')

        # Rollback.
        self.kernel.exec_function(app__config__set, {
            'key': 'global.name',
            'value': 'wex'
        })

        self.assertEqual(self.kernel.exec_function(
            app__config__get,
            {
                'key': 'global.name'
            }
        ), 'wex')
