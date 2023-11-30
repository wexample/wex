from typing import TYPE_CHECKING

from src.const.globals import COMMAND_TYPE_ADDON
from src.core.response.InteractiveShellCommandResponse import (
    InteractiveShellCommandResponse,
)
from src.decorator.command import command

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Return an int value", command_type=COMMAND_TYPE_ADDON)
def test__return_type__interactive_shell_command(kernel: "Kernel") -> InteractiveShellCommandResponse:
    return InteractiveShellCommandResponse(
        kernel, ["echo", "INTERACTIVE_SHELL_COMMAND_RESPONSE"]
    )
