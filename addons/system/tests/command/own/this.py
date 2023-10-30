import os

from addons.system.command.own.this import system__own__this
from src.helper.system import get_user_or_sudo_user
from src.const.globals import OWNER_USERNAME
from src.helper.file import get_file_owner
from tests.AbstractTestCase import AbstractTestCase


class TestSystemCommandOwnThis(AbstractTestCase):
    def test_this(self):
        test_file = self.build_test_file('config_bash')

        os.chown(
            test_file,
            0,
            0,
        )

        self.kernel.run_function(system__own__this, {
            'path': self.kernel.get_or_create_path('tmp')
        })

        owner = get_user_or_sudo_user()

        self.assertEqual(
            get_file_owner(
                test_file
            ),
            owner
        )

        self.kernel.run_function(system__own__this, {
            'path': test_file
        })

        self.assertEqual(
            get_file_owner(
                test_file
            ),
            owner
        )
