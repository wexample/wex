from __future__ import annotations

from typing import TYPE_CHECKING
from src.const.types import ShellCommandResponseTuple
from src.core.response.AbstractResponse import AbstractResponse
from src.decorator.command import command

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


@command(help="Return the current docker local ip")
def docker__docker__ip(
    kernel: Kernel,
) -> ShellCommandResponseTuple | AbstractResponse | str:
    from addons.system.command.os.name import OS_NAME_MAC, system__os__name
    from src.helper.command import command_exists, execute_command_sync
    from addons.system.command.system.ip import system__system__ip
    if kernel.run_function(system__os__name).first() == OS_NAME_MAC:
        return "127.0.0.1"

    if command_exists("docker-machine"):
        return execute_command_sync(kernel, ["docker-machine", "ip"])
    else:
        return kernel.run_function(system__system__ip)
