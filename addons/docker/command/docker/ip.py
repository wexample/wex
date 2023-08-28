import click

from addons.system.command.os.name import system__os__name, OS_NAME_MAC
from addons.system.command.system.ip import system__system__ip
from src.helper.command import execute_command_sync, command_exists


@click.command(help="Return the current docker local ip")
@click.pass_obj
def docker__docker__ip(kernel):
    if kernel.exec_function(
            system__os__name
    ) == OS_NAME_MAC:
        return '127.0.0.1'

    if command_exists('docker-machine'):
        return execute_command_sync(kernel, [
            'docker-machine',
            'ip'
        ])
    else:
        return kernel.exec_function(
            system__system__ip
        )
