import os
import yaml

from addons.app.const.app import APP_DIR_APP_DATA
from src.decorator.option import option
from src.core import Kernel
from addons.app.decorator.app_command import app_command
from addons.app.AppAddonManager import AppAddonManager
from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse

COMMAND_TYPE_BASH = 'bash'


@app_command(help="Description")
@option('--name', '-n', type=str, required=True, help="Script name")
def app__script__exec(kernel: Kernel, app_dir: str, name: str):
    manager: AppAddonManager = kernel.addons['app']
    script_dir: str = os.path.join(
        manager.app_dir,
        APP_DIR_APP_DATA,
        'script',
        name + '.yml'
    )

    if not os.path.exists(script_dir):
        return None

    # Load the configuration file
    with open(script_dir, 'r') as file:
        script = yaml.safe_load(file)

    commands_collection = []

    # Iterate through each command in the configuration
    for script_part in script.get('scripts', []):
        if isinstance(script_part, str):
            script_part = {
                'script': script_part,
                'title': script_part,
                'type': COMMAND_TYPE_BASH
            }

        script_part_type = script_part.get('type', COMMAND_TYPE_BASH)

        script = None

        if script_part_type == COMMAND_TYPE_BASH:
            script = script_part.get('script', '')

        if script:
            commands_collection.append(
                InteractiveShellCommandResponse(kernel, script)
            )

    return ResponseCollectionResponse(kernel, commands_collection)
