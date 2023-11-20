from src.helper.command import execute_command
from src.decorator.command import command
from src.decorator.option import option
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Return true if docker container runs")
@option('--name', '-n', type=str, required=True, help="Container name")
@option('--all', '-a', is_flag=True, required=False, default=False, help="Include stopped ones")
def docker__container__runs(kernel: 'Kernel', name: str, all: bool = False):
    command = [
        'docker',
        'ps',
    ]

    if all:
        command.append('-a')

    command.extend([
        '--filter',
        'name=' + name,
        '--format',
        '{{.Names}}'
    ])

    success, content = execute_command(
        kernel,
        command,
    )

    return success and len(content) > 0 and content[0] == name
