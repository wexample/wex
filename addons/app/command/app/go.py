from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.hook.exec import app__hook__exec
from src.helper.dict import get_dict_item_by_path
from src.helper.command import command_to_string
from src.core import Kernel
from src.decorator.command import command
from src.decorator.option import option
from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from src.decorator.alias import alias


@command(help="Enter into app container")
@alias('app/go')
@app_dir_option()
@option('--container', '-c', type=str, required=False, help="Container name if not configured")
@option('--user', '-u', type=str, required=False, help="User name or uid")
def app__app__go(kernel: Kernel, app_dir: str, container: str | None = None, user: str | None = None):
    manager: AppAddonManager = kernel.addons['app']

    container = manager.get_config(f'docker.main_service', container)

    if not container:
        manager.log('No main container configured')
        return

    command = [
        'docker',
        'exec',
        '-ti',
    ]

    if user:
        command += [
            '-u',
            user
        ]

    # Allow to use /bin/bash or /bin/sh, or something else.
    shell_command = get_dict_item_by_path(
        kernel.registry,
        f'services.{container}.config.container.shell',
        '/bin/bash'
    )

    command += [
        f'{manager.get_runtime_config("name")}_{container}',
        shell_command
    ]

    enter_command = kernel.run_function(
        app__hook__exec,
        {
            'app-dir': app_dir,
            'arguments': {
                'container': container
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

    if sub_command and len(sub_command):
        sub_command += [
            '&&',
            shell_command
        ]

        command += [
            '-c',
            command_to_string(sub_command),
        ]

    return InteractiveShellCommandResponse(
        kernel,
        command
    )
