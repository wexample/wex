import os

from addons.app.const.app import APP_FILEPATH_REL_CONFIG
from addons.app.command.app.perms import app__app__perms
from addons.app.helpers.test import DEFAULT_APP_TEST_NAME
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from addons.app.AppAddonManager import AppAddonManager
from src.const.globals import ROOT_USERNAME, USER_WWW_DATA
from src.helper.system import get_uid_from_user_name, get_gid_from_group_name, get_sudo_username, get_user_group_name
from src.helper.file import get_file_owner, get_file_group


class TestAppCommandAppPerms(AbstractAppTestCase):
    def test_perms(self):
        app_dir = self.create_test_app(
            DEFAULT_APP_TEST_NAME,
            force_restart=True)

        test_file = os.path.join(
            app_dir,
            APP_FILEPATH_REL_CONFIG
        )

        os.chmod(
            test_file,
            0o777
        )

        os.chown(
            test_file,
            get_uid_from_user_name(ROOT_USERNAME),
            get_gid_from_group_name(ROOT_USERNAME)
        )

        self.assertEqual(
            get_file_owner(
                test_file
            ),
            ROOT_USERNAME
        )

        self.kernel.run_function(
            app__app__perms,
            {
                'app-dir': app_dir
            }
        )

        self.assertEqual(
            get_file_owner(
                test_file
            ),
            USER_WWW_DATA
        )

        # Use config
        manager = AppAddonManager(self.kernel, app_dir)

        current_user = get_sudo_username()
        current_group = get_user_group_name(current_user)

        manager.set_config('permissions.user', current_user)
        manager.set_config('permissions.group', current_group)

        self.kernel.run_function(
            app__app__perms,
            {
                'app-dir': app_dir
            }
        )

        self.assertEqual(
            get_file_owner(
                test_file
            ),
            current_user
        )

        self.assertEqual(
            get_file_group(
                test_file
            ),
            current_group
        )
