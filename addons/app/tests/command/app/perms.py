import os

from addons.app.const.app import APP_FILEPATH_REL_CONFIG
from addons.app.command.app.perms import app__app__perms
from src.const.globals import ROOT_USERNAME, OWNER_USERNAME
from src.helper.system import get_uid_from_user_name, get_gid_from_group_name
from src.helper.file import get_file_owner
from tests.AbstractTestCase import AbstractTestCase
from addons.app.helpers.test import create_test_app


class TestAppCommandAppPerms(AbstractTestCase):
    def test_perms(self):
        app_dir = create_test_app(self.kernel)
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

        self.kernel.exec_function(
            app__app__perms,
            {
                'app-dir': app_dir
            }
        )

        self.assertEqual(
            get_file_owner(
                test_file
            ),
            OWNER_USERNAME
        )