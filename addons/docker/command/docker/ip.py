from addons.system.command.os.name import system__os__name, OS_NAME_MAC
from addons.system.command.system.ip import system__system__ip
from src.helper.command import execute_command_sync, command_exists
from src.decorator.command import command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Return the current docker local ip")
def docker__docker__ip(kernel: 'Kernel'):
    if kernel.run_function(
            system__os__name
    ).first() == OS_NAME_MAC:
        return '127.0.0.1'

    if command_exists('docker-machine'):
        return execute_command_sync(kernel, [
            'docker-machine',
            'ip'
        ])
    else:
        return kernel.run_function(
            system__system__ip
        )
