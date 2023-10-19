import os

from addons.core.command.test.create import core__test__create
from src.const.globals import COMMAND_TYPE_CORE, COMMAND_TYPE_ADDON, COMMAND_CHAR_USER
from src.helper.file import create_from_template
from src.decorator.command import command
from src.decorator.option import option
from src.core.Kernel import Kernel


@command(help="Create a new command and test files")
@option('--command', '-c', type=str, required=True,
        help="Full name of the command, i.e. addon::some/thing")
@option('--force', '-f', type=bool, required=False, is_flag=True, default=False,
        help='Force to create file if exists')
def core__command__create(kernel: Kernel, command: str, force: bool = False) -> {}:
    kernel.io.log('Creating command file...')
    request = kernel.create_command_request(command)

    if not request:
        kernel.io.message(f'Unable to process command : {command}')
        return

    command_path: str = request.resolver.build_path_or_fail(request)

    # File exists
    if not os.path.exists(command_path) or force:
        command_type = request.resolver.get_type()

        if command_type == COMMAND_TYPE_CORE:
            kernel.io.message(f'Unable to create core command : {command}')
            return
        # User wants to create some/command, but with no addons name
        # So we suggest user want to create a local user command.
        elif command_type == COMMAND_TYPE_ADDON:
            if not command_path:
                kernel.io.log('No given addon name, creating a local user command...')

                return kernel.run_function(
                    core__command__create,
                    {
                        'command': f'{COMMAND_CHAR_USER}{command}'
                    }
                ).first()

        os.makedirs(
            os.path.dirname(command_path),
            exist_ok=True
        )

        function_name = request.resolver.get_function_name(
            list(request.match.groups())
        )

        create_from_template(
            kernel.path['templates'] + 'command.py.tpl',
            command_path,
            {
                'function_name': function_name,
                'command_type_constant': f'COMMAND_TYPE_{command_type.upper()}',
            }
        )

        kernel.io.message(f'Created command file : {command_path}')

    test_file = kernel.run_function(
        core__test__create,
        {
            'command': command
        }
    ).first()

    kernel.rebuild()

    kernel.io.log('Giving files permission...')
    request.resolver.set_command_file_permission(command_path)
    request.resolver.set_command_file_permission(test_file)

    return {
        'command': command_path,
        'test': test_file
    }
