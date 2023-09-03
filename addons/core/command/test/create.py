from src.helper.registry import get_all_commands_from_addons
from src.helper.test import create_test_from_command
from src.decorator.as_sudo import as_sudo
from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.option import option


@command()
@as_sudo
@option('--all', '-a', type=str, is_flag=True, required=False, help="Create all missing tests")
@option('--command', '-c', type=str, required=False, help="Command name")
@option('--force', '-f', type=bool, required=False, is_flag=True, default=False,
        help='Force to create file if exists')
def core__test__create(kernel: Kernel, command: str = None, all: bool = False, force: bool = False) -> str | list:
    if not command:
        if all:
            output = []

            # Create all missing tests
            for command, command_data in get_all_commands_from_addons(kernel).items():
                output.append(create_test_from_command(kernel, command, force))

            return output
    else:
        return create_test_from_command(kernel, command, force)
