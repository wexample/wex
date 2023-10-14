from src.decorator.command import command
from src.decorator.option import option
from src.core import Kernel
from src.helper.system import get_processes_by_port, kill_process
from src.decorator.as_sudo import as_sudo


@command(help="Description")
@as_sudo
@option('--port', '-p', type=int, required=True, help="Port number")
def system__kill__by_port(kernel: Kernel, port: int):
    process = get_processes_by_port(port)

    if process:
        kill_process(process)

    return process
