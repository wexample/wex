import os
import shutil

from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.app.perms import app__app__perms
from addons.app.const.app import APP_DIR_TMP, APP_FILEPATH_REL_CONFIG
from addons.app.helper.test import DEFAULT_APP_TEST_NAME
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from src.const.globals import ROOT_USERNAME, USER_WWW_DATA
from src.helper.file import file_get_group, file_get_owner
from src.helper.user import (get_gid_from_group_name, get_sudo_username,
                             get_uid_from_user_name, get_user_group_name,
                             get_user_or_sudo_user)


class TestAppCommandAppPerms(AbstractAppTestCase):
    def test_perms(self) -> None:
        app_dir = self.create_test_app(DEFAULT_APP_TEST_NAME, force_restart=True)

        test_file = os.path.join(app_dir, APP_FILEPATH_REL_CONFIG)

        os.chmod(test_file, 0o777)

        os.chown(
            test_file,
            get_uid_from_user_name(ROOT_USERNAME),
            get_gid_from_group_name(ROOT_USERNAME),
        )

        self.assertEqual(file_get_owner(test_file), ROOT_USERNAME)

        self.kernel.run_function(app__app__perms, {"app-dir": app_dir})

        self.assertTrue(
            file_get_owner(test_file) in [USER_WWW_DATA, get_user_or_sudo_user()]
        )

        # Reuse manager to work with
        manager = AppAddonManager(self.kernel, app_dir=app_dir)

        current_user = get_sudo_username()
        assert current_user is not None
        current_group = get_user_group_name(current_user)

        manager.set_config("permissions.user", current_user)
        manager.set_config("permissions.group", current_group)

        self.reload_app_manager()

        tmp_dir = f"{app_dir}{APP_DIR_TMP}"
        # Will be recreated by perms command
        shutil.rmtree(tmp_dir)

        self.log("Current user is " + current_user)
        self.log("Application path is " + app_dir)

        self.kernel.run_function(app__app__perms, {"app-dir": app_dir})

        self.assertEqual(file_get_owner(test_file), current_user)
        self.assertEqual(file_get_group(test_file), current_group)
        self.assertTrue(os.path.exists(tmp_dir), "Temp dir has been recreated")
