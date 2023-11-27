from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from src.decorator.option import option
from src.helper.test import create_test_from_command
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@as_sudo()
@command(help="Create a test file for command")
@option('--all', '-a', type=str, is_flag=True, required=False, help="Create all missing tests")
@option('--command', '-c', type=str, required=False, help="Command name")
@option('--force', '-f', type=bool, required=False, is_flag=True, default=False,
        help='Force to create file if exists')
def core__test__create(kernel: 'Kernel', command: Optional[str] = None, all: bool = False, force: bool = False) -> str | list:
    if not command and all:
        output = []

        # Create all missing tests
        for command, command_data in kernel.resolvers[COMMAND_TYPE_ADDON].get_commands_registry().commands.items():
            output.append(create_test_from_command(kernel, command, force))

        return output
    else:
        return create_test_from_command(kernel, command, force)
