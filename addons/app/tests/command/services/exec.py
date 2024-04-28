from addons.app.command.services.exec import app__services__exec
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from src.const.globals import COMMAND_CHAR_SERVICE


class TestAppCommandServicesExec(AbstractAppTestCase):
    def test_exec(self) -> None:
        app_dir = self.create_and_start_test_app(services=["php"])

        response = self.kernel.run_function(
            app__services__exec, {"app-dir": app_dir, "hook": "hook/name"}
        )

        # The command does not exist
        self.assertEqual(response.first()[f"{COMMAND_CHAR_SERVICE}php"].print(), None)
