from typing import TYPE_CHECKING

from src.const.globals import COMMAND_TYPE_ADDON
from src.core.response.NonInteractiveShellCommandResponse import (
    NonInteractiveShellCommandResponse,
)
from src.decorator.command import command

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Return an int value", command_type=COMMAND_TYPE_ADDON)
def test__return_type__non_interactive_shell_command(kernel: "Kernel") -> NonInteractiveShellCommandResponse:
    return NonInteractiveShellCommandResponse(
        kernel, ["echo", "NON_INTERACTIVE_SHELL_COMMAND_RESPONSE"]
    )
