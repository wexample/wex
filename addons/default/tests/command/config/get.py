from tests.AbstractTestCase import AbstractTestCase


class TestDefaultCommandConfigGet(AbstractTestCase):
    def test_get(self):
        file = self.build_test_file_path('config_bash')

        value = self.kernel.exec('default::config/get', {
            'file': file,
            'key': 'DOLOR'
        })

        self.assertEqual(value, 'sit')

        value = self.kernel.exec('default::config/get', {
            'file': file,
            'key': 'UNKNOWN_KEY',
            'default': 'default value'
        })

        self.assertEqual(value, 'default value')
