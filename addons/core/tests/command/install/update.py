from addons.core.command.install.update import core__install__update
from src.const.globals import COMMAND_TYPE_ADDON
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandInstallUpdate(AbstractTestCase):
    def test_update(self) -> None:
        request = self.kernel.create_command_request(
            self.kernel.get_command_resolver(
                COMMAND_TYPE_ADDON
            ).build_command_from_function(core__install__update),
        )

        self.assertIsNotNone(
            request.get_string_command(),
        )

        self.assertIsNotNone(
            request.get_script_command(),
        )
