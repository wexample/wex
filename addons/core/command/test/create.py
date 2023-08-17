import click

from src.helper.registry import get_all_commands
from src.helper.test import create_test_from_command
from src.decorator.as_sudo import as_sudo


@click.command
@as_sudo
@click.pass_obj
@click.option('--command', '-c', type=str, required=False, help="Command name, if empty it will create all missing "
                                                                "tests")
def core__test__create(kernel, command: str = None) -> list:
    if not command:
        output = []

        # Create all missing tests
        for command, command_data in get_all_commands(kernel).items():
            output.append(create_test_from_command(kernel, command))

        return output
    else:
        return [create_test_from_command(kernel, command)]
