from addons.app.command.config.get import app__config__get
from tests.AbstractTestCase import AbstractTestCase
from addons.app.helpers.test import create_test_app


class TestAppCommandConfigGet(AbstractTestCase):
    def test_get(self):
        app_dir = create_test_app(self.kernel)

        value = self.kernel.run_function(app__config__get, {
            'key': 'global.name',
            'app-dir': app_dir
        })

        self.assertEqual(value, 'test_app')
