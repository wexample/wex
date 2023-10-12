from src.const.globals import COMMAND_CHAR_SERVICE, COMMAND_SEPARATOR_ADDON
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandDbGo(AbstractAppTestCase):
    def test_go(self):
        db_service = 'mysql_8'
        app_dir = self.create_and_start_test_app(services=['php_8'])

        go_command = self.kernel.run_command(
            f'{COMMAND_CHAR_SERVICE}{db_service}{COMMAND_SEPARATOR_ADDON}db/go',
            {
                'app-dir': app_dir,
                'service': db_service
            }
        ).first()

        self.assertEqual(
            go_command,
            'mysql --defaults-extra-file=/tmp/mysql.cnf'
        )
