from addons.app.command.config.get import app__config__get
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandConfigGet(AbstractAppTestCase):
    def test_get(self):
        app_dir = self.create_and_start_test_app(services=['php'])

        value = self.kernel.run_function(app__config__get, {
            'key': 'global.name',
            'app-dir': app_dir
        }).first()

        self.assertEqual(value, 'test_app')
