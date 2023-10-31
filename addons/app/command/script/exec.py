import os
import yaml

from addons.app.const.app import APP_DIR_APP_DATA, ERR_APP_SHOULD_RUN
from src.decorator.option import option
from src.core import Kernel
from addons.app.decorator.app_command import app_command
from addons.app.AppAddonManager import AppAddonManager
from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from addons.app.command.app.started import app__app__started

COMMAND_TYPE_BASH = 'bash'
COMMAND_TYPE_BASH_FILE = 'bash-file'
COMMAND_TYPE_PYTHON = 'python'
COMMAND_TYPE_PYTHON_FILE = 'python-file'


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

        if 'container_name' in script_part:
            script_part['app_should_run'] = True

        if 'app_should_run' in script_part:
            if not kernel.run_function(
                    app__app__started,
                    {
                        'app-dir': app_dir,
                    }
            ).first():
                kernel.io.error(ERR_APP_SHOULD_RUN, {
                    'command': kernel.request.command,
                    'dir': app_dir,
                })

                return

        if script_part_type == COMMAND_TYPE_BASH:
            script = script_part.get('script', '')
        elif script_part_type == COMMAND_TYPE_BASH_FILE:
            script = [
                'bash',
                os.path.join(
                    manager.app_dir,
                    script_part['file']
                )
            ]
        # elif script_part_type == COMMAND_TYPE_PYTHON:
        # elif script_part_type == COMMAND_TYPE_PYTHON_FILE:

        if script:
            commands_collection.append(
                InteractiveShellCommandResponse(kernel, script)
            )

    return ResponseCollectionResponse(kernel, commands_collection)
