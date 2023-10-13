from src.helper.args import parse_arg
from src.helper.command import command_to_string
from src.decorator.command import command
from src.decorator.option import option
from src.core import Kernel
from src.decorator.alias import alias
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.hook.exec import app__hook__exec
from src.core.response.NonInteractiveShellCommandResponse import NonInteractiveShellCommandResponse
from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from src.helper.dict import get_dict_item_by_path
from addons.app.decorator.app_should_run import app_should_run


@command(help="Exec a command into app container")
@alias('app/exec')
@app_should_run
@app_dir_option()
@option('--container-name', '-cn', type=str, required=False, help="Container name if not configured")
@option('--command', '-c', type=str, required=True, help="Command to execute")
@option('--user', '-u', type=str, required=False, help="User name or uid")
@option('--sync', '-s', type=bool, is_flag=True, required=False, help="Execute command in a sub process")
def app__app__exec(
        kernel: Kernel,
        app_dir: str,
        command: str,
        container_name: str | None = None,
        user: str | None = None,
        sync: bool = False):
    manager: AppAddonManager = kernel.addons['app']
    container_name = container_name or manager.get_config(f'docker.main_container', None)

    if not container_name:
        manager.log('No main container configured')
        return

    docker_command = [
        'docker',
        'exec',
        '-ti',
    ]

    if user:
        docker_command += [
            '-u',
            user
        ]

    # Allow to use /bin/bash or /bin/sh, or something else.
    shell_command = get_dict_item_by_path(
        kernel.registry,
        f'services.{container_name}.config.container.shell',
        '/bin/bash'
    )

    docker_command += [
        f'{manager.get_runtime_config("name")}_{container_name}',
        shell_command
    ]

    enter_command = kernel.run_function(
        app__hook__exec,
        {
            'app-dir': app_dir,
            'arguments': {
                'container': container_name
            },
            'hook': 'app/exec',
        }
    )

    result = enter_command.first()
    sub_command = []
    for index in result:
        if result[index]:
            # Last result overrides previous to avoid
            # merging which can result to an unexpected final command
            sub_command = result[index].first()

    # Convert command in list to string
    command = parse_arg(command)
    if isinstance(command, list):
        command = command_to_string(command)

    # Prepare the final command to be executed
    final_command = []

    if sub_command and len(sub_command):
        final_command += sub_command
        final_command += ['&&']

    # Add the main command
    final_command += [command]

    # Append the final command to docker_command
    docker_command += ['-c', command_to_string(final_command, add_quotes=False)]

    if sync:
        return NonInteractiveShellCommandResponse(
            kernel,
            docker_command
        )

    return InteractiveShellCommandResponse(
        kernel,
        docker_command
    )
