import os
import types
import click
import builtins

from click import Command

from src.helper.command import apply_command_decorator
from src.helper.dict import dict_get_item_by_path
from src.helper.data_yaml import yaml_load
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

    def build_script_command(self) -> Command:
        def _script_command_handler(*args, **kwargs):
            commands_collection = []

            variables = {}
            for name in kwargs:
                variables[name.upper()] = kwargs[name]

            variables.update({
                'PATH_CORE': self.kernel.get_path('root'),
                'PATH_CURRENT': os.getcwd() + os.sep
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

                command = script_command.run_script(
                    script_command.function,
                    self,
                    script,
                    variables
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

        internal_command = self.request.resolver.get_function_name(
            self.request.resolver.build_command_parts_from_file_path(self.request.path)
        )
        # Function must have the appropriate name,
        # allowing to guess internal command name from it
        click_function_callback = types.FunctionType(
            _script_command_handler.__code__,
            _script_command_handler.__globals__,
            internal_command,
            _script_command_handler.__defaults__,
            _script_command_handler.__closure__
        )

        decorator_name = dict_get_item_by_path(self.content, 'command.decorator')
        if decorator_name:
            decorator = self.kernel.decorators['command'][decorator_name]
        else:
            decorator = command

        if 'help' not in self.content:
            self.kernel.io.error(
                f'Missing help section in command {internal_command}',
                trace=False)

        decorator_options = dict_get_item_by_path(self.content, 'command.options', {})
        script_command = decorator(help=self.content['help'], **decorator_options)(click_function_callback)

        # Apply extra decorators
        properties = dict_get_item_by_path(
            data=self.content,
            key='properties',
            default=[]) or []

        for property in properties:
            if isinstance(property, str):
                name = property
                value = None
            else:
                name = list(property.keys())[0]
                value = property[name]

            script_command = apply_command_decorator(
                self.kernel,
                function=script_command,
                group='properties',
                name=name,
                options=value
            )

        if 'options' in self.content:
            options = self.content['options']

            for option in options:
                script_command.function = click.option(
                    option['name'],
                    option['short'],
                    default=option['default'] if 'default' in option else False,
                    help=option['help'] if 'help' in option else None,
                    is_flag='is_flag' in option and option['is_flag'],
                    required=option['required'] if 'required' in option else False,
                    type=getattr(builtins, option['type'] if 'type' in option else 'any'),
                )(script_command.function)

        return script_command

    def run(self):
        return self.run_click_function(
            self.request.function
        )
