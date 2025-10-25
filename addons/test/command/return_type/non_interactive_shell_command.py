from __future__ import annotations

from typing import TYPE_CHECKING

from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.command import command

if TYPE_CHECKING:
    from src.utils.kernel import Kernel
    from src.core.response.NonInteractiveShellCommandResponse import (
        NonInteractiveShellCommandResponse,
    )


@command(help="Return an int value", command_type=COMMAND_TYPE_ADDON)
def test__return_type__non_interactive_shell_command(
    kernel: Kernel,
) -> NonInteractiveShellCommandResponse:
    from src.core.response.NonInteractiveShellCommandResponse import (
        NonInteractiveShellCommandResponse,
    )

    return NonInteractiveShellCommandResponse(
        kernel, ["echo", "NON_INTERACTIVE_SHELL_COMMAND_RESPONSE"]
    )
