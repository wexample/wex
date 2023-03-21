import click
import os

from src.helper.file import create_from_template

from src.helper.command import build_function_name_from_match


@click.command()
@click.pass_obj
@click.option('--command', '-c', type=str, required=True, help="Full name of the command, i.e. addon::some/thing")
def core_command_create(kernel, command: str) -> {}:
    kernel.log('Creating command file...')

    match = kernel.build_match_or_fail(command)

    command_path: str = kernel.build_command_path_from_match(match)
    dir = os.path.dirname(command_path)
    function_name = build_function_name_from_match(match)

    os.makedirs(dir, exist_ok=True)

    create_from_template(
        kernel.path['templates'] + 'command.py.tpl',
        command_path,
        {
            'function_name': function_name,
        }
    )

    kernel.log_notice(f'Created command file : {command_path}')

    test_file = kernel.exec(f'test-create', [command])

    return {
        'command': command_path,
        'test': test_file
    }
