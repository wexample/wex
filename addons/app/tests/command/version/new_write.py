from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.version.new_write import app__version__new_write
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from src.const.globals import VERSION_DEFAULT


class TestAppCommandVersionNewWrite(AbstractAppTestCase):
    def test_new_write(self) -> None:
        manager = AppAddonManager(self.kernel, app_dir=self.kernel.directory.path)
        manager.load_config()

        current_version = manager.get_config("global.version").get_str()
        app_dir = self.create_test_app()

        # Change version.
        version = self.kernel.run_function(
            app__version__new_write, {"version": VERSION_DEFAULT, "app-dir": app_dir}
        ).first()

        self.assertEqual(version, VERSION_DEFAULT)

        # Rollback.
        self.kernel.run_function(
            app__version__new_write, {"version": current_version, "app-dir": app_dir}
        )
