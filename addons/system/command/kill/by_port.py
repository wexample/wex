from typing import TYPE_CHECKING

from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from src.decorator.option import option
from src.helper.process import process_get_all_by_port, process_kill

if TYPE_CHECKING:
    from src.core.Kernel import Kernel

@as_sudo()
@command(help="Description")
@option('--port', '-p', type=int, required=True, help="Port number")
def system__kill__by_port(kernel: 'Kernel', port: int):
    process = process_get_all_by_port(port)

    if process:
        process_kill(process)

    return process
