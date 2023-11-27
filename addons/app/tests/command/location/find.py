import os

from addons.app.command.location.find import app__location__find
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandLocationFind(AbstractTestCase):
    def test_find(self):
        # Test without dir argument.
        app_location = self.kernel.run_function(app__location__find).first()
        self.assertEqual(app_location, self.kernel.get_path("root"))

        cwd = os.getcwd()
        tmp_dir = self.kernel.get_or_create_path("tmp")
        root_dir = self.kernel.get_path("root")

        # Change to a dir inside the app and test again.
        os.chdir(tmp_dir)
        app_location = self.kernel.run_function(app__location__find).first()
        self.assertEqual(app_location, root_dir)

        # Change to root, no app dir should be found.
        app_location = self.kernel.run_function(
            app__location__find, {"app-dir": "/var/tmp"}
        ).first()
        self.assertEqual(app_location, None)

        # Change from root with argument to a dir inside the app and test again.
        app_location = self.kernel.run_function(
            app__location__find, {"app-dir": tmp_dir}
        ).first()
        self.assertEqual(app_location, root_dir)

        os.chdir(cwd)
