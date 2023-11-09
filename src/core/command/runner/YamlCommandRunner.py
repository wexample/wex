import os
import sys

import click
from click import Command

from src.helper.string import replace_variables
from src.helper.yaml import yaml_load
from src.const.error import ERR_UNEXPECTED
from src.core.command.runner.AbstractCommandRunner import AbstractCommandRunner
from src.core.CommandRequest import CommandRequest
from src.decorator.command import command
from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse

COMMAND_TYPE_BASH = 'bash'
COMMAND_TYPE_BASH_FILE = 'bash-file'
COMMAND_TYPE_PYTHON = 'python'
COMMAND_TYPE_PYTHON_FILE = 'python-file'


class YamlCommandRunner(AbstractCommandRunner):
    def __init__(self, kernel):
        super().__init__(kernel)

    def set_request(self, request: CommandRequest):
        super().set_request(request=request)

        self.content = yaml_load(self.request.path)

        if not self.content:
            self.kernel.io.error(ERR_UNEXPECTED, {
                'error': f'Unable to load yaml script file content :  {self.request.path}',
            })

    def convert_args_dict_to_list(self, args: dict) -> list:
        pass

    def get_request_function(self, path: str, parts) -> Command:
        pass

    def get_params(self) -> list:
        pass

    def get_command_type(self):
        return self.content['type']

    def get_attr(self, name: str, default=None) -> bool:
        pass

    def has_attr(self, name: str) -> bool:
        pass

    def run(self):
        def _click_function_handler(*args, **kwargs):
            commands_collection = []
            env_args = kwargs.copy()

            env_args.update({
                'path_core': self.kernel.get_path('root'),
                'path_current': os.getcwd() + os.sep
            })

            # Iterate through each command in the configuration
            for script in self.content.get('scripts', []):
                if isinstance(script, str):
                    script = {
                        'script': script,
                        'title': script,
                        'type': COMMAND_TYPE_BASH
                    }

                self.kernel.io.log(script['title'])

                if 'script' in script:
                    script['script'] = replace_variables(
                        script['script'], env_args)

                if 'file' in script:
                    script['file'] = replace_variables(
                        script['file'], env_args)

                script_part_type = script.get('type', COMMAND_TYPE_BASH)
                command = None
                if script_part_type == COMMAND_TYPE_BASH:
                    command = script.get('script', '')
                elif script_part_type == COMMAND_TYPE_BASH_FILE:
                    # File is required in this case.
                    if 'file' in script_part_type:
                        command = [
                            'bash',
                            script['file']
                        ]
                elif script_part_type == COMMAND_TYPE_PYTHON:
                    if 'script' in script:
                        command = [
                            sys.executable,
                            '-c',
                            script['script']
                        ]
                elif script_part_type == COMMAND_TYPE_PYTHON_FILE:
                    # File is required in this case.
                    if 'file' in script_part_type:
                        command = [
                            'python3',
                            script['file']
                        ]

                if command:
                    if 'container_name' in script:
                        pass
                    else:
                        commands_collection.append(
                            InteractiveShellCommandResponse(self.kernel, command)
                        )

            return QueuedCollectionResponse(self.kernel, commands_collection)

        click_function = command(help=self.content['help'])(_click_function_handler)

        if 'options' in self.content:
            options = self.content['options']

            for option in options:
                click_function = click.option(
                    option['name'],
                    option['short'],
                    is_flag='is_flag' in option and option['is_flag'],
                    required=option['required'],
                    help=option['help']
                )(click_function)

        return self.run_click_function(
            click_function
        )
