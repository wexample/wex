from src.core.response.NonInteractiveShellCommandResponse import NonInteractiveShellCommandResponse
from src.helper.command import command_to_string
from src.decorator.command import command
from src.decorator.option import option
from src.core import Kernel
from src.decorator.alias import alias
from addons.app.command.app.started import app__app__started, APP_STARTED_CHECK_MODE_ANY_CONTAINER
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.hook.exec import app__hook__exec
from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from src.helper.dict import get_dict_item_by_path


@command(help="Exec a command into app container")
@alias('app/exec')
@app_dir_option()
@option('--container-name', '-cn', type=str, required=False, help="Container name if not configured")
@option('--command', '-c', type=str, required=True, help="Command to execute")
@option('--user', '-u', type=str, required=False, help="User name or uid")
def app__app__exec(
        kernel: Kernel,
        app_dir: str,
        command: str,
        container_name: str | None = None,
        user: str | None = None):
    manager: AppAddonManager = kernel.addons['app']
    container_name = manager.get_config(f'docker.main_container', container_name)

    if not kernel.run_function(app__app__started, {
        'app-dir': app_dir,
        'mode': APP_STARTED_CHECK_MODE_ANY_CONTAINER
    }).first():
        manager.log('App not running')
        return

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
            'hook': 'app/go',
        }
    )

    result = enter_command.first()
    sub_command = []
    for index in result:
        if result[index]:
            # Last result overrides previous to avoid
            # merging which can result to an unexpected final command
            sub_command = result[index].first()

    # Prepare the final command to be executed
    final_command = []

    if sub_command and len(sub_command):
        final_command += sub_command
        final_command += ['&&']

    # Add the main command
    final_command += [command]

    # Append the final command to docker_command
    docker_command += ['-c', command_to_string(final_command, add_quotes=False)]

    return InteractiveShellCommandResponse(
        kernel,
        docker_command
    )
