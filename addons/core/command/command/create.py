import click
import os

from addons.core.command.test.create import core__test__create
from src.helper.file import create_from_template
from src.helper.command import build_function_name_from_match, build_command_path_from_match


@click.command()
@click.pass_obj
@click.option('--command', '-c', type=str, required=True, help="Full name of the command, i.e. addon::some/thing")
def core__command__create(kernel, command: str) -> {}:
    kernel.log('Creating command file...')
    match, command_type = kernel.build_match_or_fail(command)
    function_name = build_function_name_from_match(match, command_type)
    command_path: str = build_command_path_from_match(kernel, match, command_type)

    os.makedirs(
        os.path.dirname(command_path),
        exist_ok=True
    )

    create_from_template(
        kernel.path['templates'] + 'command.py.tpl',
        command_path,
        {
            'function_name': function_name,
        }
    )

    kernel.message(f'Created command file : {command_path}')

    test_file = kernel.exec_function(core__test__create, {
        'command': command
    })

    return {
        'command': command_path,
        'test': test_file
    }
