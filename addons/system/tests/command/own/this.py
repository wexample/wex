import os

from addons.system.command.own.this import system__own__this
from src.const.globals import OWNER_USERNAME
from src.helper.file import get_file_owner
from tests.AbstractTestCase import AbstractTestCase


class TestSystemCommandOwnThis(AbstractTestCase):
    def test_this(self):
        test_file = self.build_test_file_path('config_bash')

        os.chown(
            test_file,
            0,
            0,
        )

        self.kernel.run_function(system__own__this, {
            'path': self.kernel.path['tmp']
        })

        self.assertEqual(
            get_file_owner(
                test_file
            ),
            OWNER_USERNAME
        )

        self.kernel.run_function(system__own__this, {
            'path': test_file
        })

        self.assertEqual(
            get_file_owner(
                test_file
            ),
            OWNER_USERNAME
        )
