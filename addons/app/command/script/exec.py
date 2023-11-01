import os

from addons.app.const.app import ERR_APP_SHOULD_RUN
from src.decorator.option import option
from src.core import Kernel
from addons.app.decorator.app_command import app_command
from addons.app.AppAddonManager import AppAddonManager
from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from addons.app.command.app.started import app__app__started
from addons.app.command.app.exec import app__app__exec

COMMAND_TYPE_BASH = 'bash'
COMMAND_TYPE_BASH_FILE = 'bash-file'
COMMAND_TYPE_PYTHON = 'python'
COMMAND_TYPE_PYTHON_FILE = 'python-file'


@app_command(help="Description")
@option('--name', '-n', type=str, required=True, help="Script name")
def app__script__exec(kernel: Kernel, app_dir: str, name: str):
    manager: AppAddonManager = kernel.addons['app']
    script_config = manager.load_script(name)

    if not script_config:
        return None

    commands_collection = []
    counter = 0
    # Iterate through each command in the configuration
    for script in script_config.get('scripts', []):
        if isinstance(script, str):
            script = {
                'script': script,
                'title': script,
                'type': COMMAND_TYPE_BASH
            }

        script_part_type = script.get('type', COMMAND_TYPE_BASH)
        command = None
        counter += 1

        if 'container_name' in script:
            script['app_should_run'] = True

        if 'app_should_run' in script:
            if not kernel.run_function(
                    app__app__started,
                    {
                        'app-dir': app_dir,
                    }
            ).first():
                kernel.io.error(ERR_APP_SHOULD_RUN, {
                    'command': script['title'],
                    'dir': app_dir,
                })

                return

        if script_part_type == COMMAND_TYPE_BASH:
            command = script.get('script', '')
        elif script_part_type == COMMAND_TYPE_BASH_FILE:
            # File is required in this case.
            if 'file' in script_part_type:
                command = [
                    'bash',
                    os.path.join(
                        manager.app_dir,
                        script['file']
                    )
                ]
        elif script_part_type == COMMAND_TYPE_PYTHON:
            if 'script' in script:
                escaped_script = script['script'].replace('"', r'\"')

                command = [
                    'python3',
                    '-c',
                    f'"{escaped_script}"'
                ]
        elif script_part_type == COMMAND_TYPE_PYTHON_FILE:
            # File is required in this case.
            if 'file' in script_part_type:
                command = [
                    'python3',
                    os.path.join(
                        manager.app_dir,
                        script['file']
                    )
                ]

        if command:
            if 'container_name' in script:
                commands_collection.append(
                    _app__script__exec__create_callback(
                        kernel, app_dir, command
                    )
                )
            else:
                commands_collection.append(
                    InteractiveShellCommandResponse(kernel, command)
                )

    return ResponseCollectionResponse(kernel, commands_collection)


def _app__script__exec__create_callback(
        kernel,
        app_dir,
        command):
    def _callback(previous):
        return kernel.run_function(
            app__app__exec,
            {
                'app-dir': app_dir,
                'command': command
            }
        )

    return _callback
