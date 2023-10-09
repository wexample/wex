from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.AppAddonManager import AppAddonManager
from src.core import Kernel
from src.decorator.command import command
from src.decorator.option import option
from src.helper.command import execute_command
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse


@command(help="Enter into app container")
@app_dir_option()
@option('--container', '-c', type=str, required=False, help="Container name if not configured")
def app__app__go(kernel: Kernel, app_dir: str, container: str | None = None):
    manager: AppAddonManager = kernel.addons['app']

    container = manager.get_config(f'docker.main_container', container)

    if not container:
        manager.log('No main container configured')
        return

    command = [
        'docker',
        'exec',
        '-ti',
        f'{manager.get_runtime_config("name")}_{container}',
        '/bin/bash'
    ]

    return ResponseCollectionResponse(kernel, [
        InteractiveShellCommandResponse(
            kernel,
            command
        )
    ])
