from addons.default.command.config.get import default_config_get
from tests.AbstractTestCase import AbstractTestCase


class TestDefaultCommandConfigSet(AbstractTestCase):
    def test_set(self):
        file = self.kernel.path['root'] + 'tests/samples/config_bash'

        # Change value.
        self.kernel.exec('default::config/set', {
            'file': file,
            'key': 'DOLOR',
            'value': 'Test value',
            'verbose': True
        })

        self.assertEqual(self.kernel.exec_function(
            default_config_get,
            {
                'file': file,
                'key': 'DOLOR'
            }
        ), 'Test value')

        # Rollback.
        self.kernel.exec('default::config/set', {
            'file': file,
            'key': 'DOLOR',
            'value': 'wex',
            'verbose': True
        })

        self.assertEqual(self.kernel.exec_function(
            default_config_get,
            {
                'file': file,
                'key': 'DOLOR'
            }
        ), 'wex')
