from addons.app.command.config.get import app__config__get
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandConfigGet(AbstractTestCase):
    def test_get(self):
        value = self.kernel.exec_function(app__config__get, {
            'key': 'global.name'
        })

        self.assertEqual(value, 'wex')
