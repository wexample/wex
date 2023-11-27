from addons.default.command.config.get import default__config__get
from tests.AbstractTestCase import AbstractTestCase


class TestDefaultCommandConfigGet(AbstractTestCase):
    def test_get(self):
        file = self.build_test_file('config_bash')

        value = self.kernel.run_function(default__config__get, {
            'file': file,
            'key': 'DOLOR'
        }).print()

        self.assertEqual(value, 'sit')

        value = self.kernel.run_function(default__config__get, {
            'file': file,
            'key': 'UNKNOWN_KEY',
            'default': 'default value'
        }).print()

        self.assertEqual(value, 'default value')
