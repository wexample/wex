import click

from src.helper.registry import get_all_commands_from_addons
from src.helper.test import create_test_from_command
from src.decorator.as_sudo import as_sudo


@click.command
@as_sudo
@click.pass_obj
@click.option('--all', '-a', type=str, is_flag=True, required=False, help="Create all missing tests")
@click.option('--command', '-c', type=str, required=False, help="Command name")
def core__test__create(kernel, command: str = None, all: bool = False) -> str | list:
    if not command:
        if all:
            output = []

            # Create all missing tests
            for command, command_data in get_all_commands_from_addons(kernel).items():
                output.append(create_test_from_command(kernel, command))

            return output
    else:
        return create_test_from_command(kernel, command)
