from addons.app.command.location.find import app__location__find
from src.helper.dir import dir_execute_in_workdir
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandLocationFind(AbstractTestCase):
    def test_find(self) -> None:
        # Test without dir argument.
        app_location = self.kernel.run_function(app__location__find).first()
        self.assertEqual(app_location, self.kernel.directory.path)

        tmp_dir = self.kernel.get_or_create_path("tmp")
        root_dir = self.kernel.directory.path

        def _test_find() -> None:
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

        dir_execute_in_workdir(tmp_dir, _test_find)
