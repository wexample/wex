from addons.app.command.location.find import app__location__find
from tests.AbstractTestCase import AbstractTestCase
import os

class TestAppCommandLocationFind(AbstractTestCase):
    def test_find(self):
        # Test without dir argument.
        app_location = self.kernel.run_function(
            app__location__find
        )
        self.assertEqual(app_location, self.kernel.path['root'])

        cwd = os.getcwd()

        # Change to a dir inside the app and test again.
        os.chdir(self.kernel.path['tmp'])
        app_location = self.kernel.run_function(app__location__find)
        self.assertEqual(app_location, self.kernel.path['root'])

        # Change to root, no app dir should be found.
        os.chdir('/')
        app_location = self.kernel.run_function(app__location__find)
        self.assertEqual(app_location, None)

        # Change from root with argument to a dir inside the app and test again.
        app_location = self.kernel.run_function(app__location__find, {
            'app-dir': self.kernel.path['tmp']
        })
        self.assertEqual(app_location, self.kernel.path['root'])

        os.chdir(cwd)
