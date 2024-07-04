from typing import TYPE_CHECKING

from src.const.globals import COMMAND_TYPE_ADDON, CORE_COMMAND_NAME
from src.core.response.InteractiveShellCommandResponse import (
    InteractiveShellCommandResponse,
)
from src.decorator.alias import alias
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


@alias("update")
@as_sudo()
@command(help="Description", command_type=COMMAND_TYPE_ADDON)
def core__install__update(kernel: "Kernel") -> InteractiveShellCommandResponse:
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
