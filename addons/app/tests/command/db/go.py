from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from src.const.globals import COMMAND_CHAR_SERVICE, COMMAND_SEPARATOR_ADDON


class TestAppCommandDbGo(AbstractAppTestCase):
    def test_go(self) -> None:
        db_service = "mysql"
        app_dir = self.create_and_start_test_app(services=["php"])

        go_command = self.kernel.run_command(
            f"{COMMAND_CHAR_SERVICE}{db_service}{COMMAND_SEPARATOR_ADDON}db/go",
            {"app-dir": app_dir, "service": db_service},
        ).first()

        self.assertEqual(go_command, "mysql --defaults-extra-file=/tmp/mysql.cnf")

        self.stop_test_app(app_dir)
