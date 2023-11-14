import os
import types

import click
from click import Command

from src.helper.dict import get_dict_item_by_path
from src.helper.yaml import yaml_load
from src.core.command.runner.AbstractCommandRunner import AbstractCommandRunner
from src.core.CommandRequest import CommandRequest
from src.decorator.command import command
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse

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
            self.kernel.io.error(f'Unable to load yaml script file content :  {self.request.path}', trace=False)

    def get_request_function(self, path: str, parts) -> Command:
        pass

    def get_params(self) -> list:
        pass

    def get_command_type(self):
        return self.content['type']

    def build_request_function(self) -> Command:
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

                command = click_function.script_run_handler(
                    click_function,
                    self,
                    script,
                    env_args
                )

                commands_collection.append(
                    InteractiveShellCommandResponse(
                        self.kernel,
                        command
                    )
                )

            return QueuedCollectionResponse(
                self.kernel,
                commands_collection)

        # Function must have the appropriate name,
        # allowing to guess internal command name from it
        click_function_callback = types.FunctionType(
            _click_function_handler.__code__,
            _click_function_handler.__globals__,
            self.request.resolver.get_function_name(
                self.request.resolver.build_command_parts_from_file_path(self.request.path)
            ),
            _click_function_handler.__defaults__,
            _click_function_handler.__closure__
        )

        decorator_name = get_dict_item_by_path(self.content, 'command.decorator')
        if decorator_name:
            decorator = self.kernel.decorators['command'][decorator_name]
        else:
            decorator = command

        decorator_options = get_dict_item_by_path(self.content, 'command.options', {})
        click_function = decorator(help=self.content['help'], **decorator_options)(click_function_callback)

        # Apply extra decorators
        properties = get_dict_item_by_path(
            data=self.content,
            key='properties',
            default=[]) or []

        for property in properties:
            name = list(property.keys())[0]

            click_function = self.kernel.apply_command_decorator(
                function=click_function,
                group='properties',
                name=name,
                options=property[name]
            )

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

        return click_function

    def run(self):
        return self.run_click_function(
            self.request.function
        )
