from __future__ import annotations

from typing import TYPE_CHECKING

from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.alias import alias
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command

if TYPE_CHECKING:
    from src.utils.kernel import Kernel
    from src.core.response.InteractiveShellCommandResponse import (
        InteractiveShellCommandResponse,
    )


@alias("update")
@as_sudo()
@command(help="Description", command_type=COMMAND_TYPE_ADDON)
def core__install__update(kernel: Kernel) -> InteractiveShellCommandResponse:
    from src.core.response.InteractiveShellCommandResponse import (
        InteractiveShellCommandResponse,
    )
    from src.const.globals import CORE_COMMAND_NAME

    return InteractiveShellCommandResponse(
        kernel,
        [
            "sudo",
            "apt",
            "update",
            "&&",
            "sudo",
            "apt",
            "install",
            "--only-upgrade",
            CORE_COMMAND_NAME,
        ],
    )
