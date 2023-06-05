import click

from src.helper.test import create_test_from_command


@click.command
@click.pass_obj
@click.option('--command', '-c', type=str, required=False, help="Command name, if empty it will create all missing "
                                                                "tests")
def core__test__create(kernel, command: str = None) -> list:
    if not command:
        output = []

        # Create all missing tests
        for command, command_data in kernel.get_all_commands().items():
            output.append(create_test_from_command(kernel, command))

        return output
    else:
        return [create_test_from_command(kernel, command)]
