from typing import Callable, TYPE_CHECKING

from src.core.command.ScriptCommand import ScriptCommand
from src.helper.command import command_escape
from src.helper.string import string_replace_multiple
from src.const.globals import SHELL_DEFAULT
from addons.app.helper.docker import docker_build_long_container_name
from src.core.FunctionProperty import FunctionProperty
from addons.app.decorator.app_dir_option import app_dir_option

if TYPE_CHECKING:
    from src.const.types import Args, Kwargs


class AppCommand(ScriptCommand):
    def __init__(self,
                 function: Callable,
                 command_type: str,
                 decorator_args: 'Args',
                 decorator_kwargs: 'Kwargs') -> None:
        # Get and pop interesting args
        dir_required = decorator_kwargs.pop('dir_required', True)
        should_run = decorator_kwargs.pop('should_run', False)

        super().__init__(
            function,
            command_type,
            decorator_args,
            decorator_kwargs,
        )

        # Do not provide app_dir to function
        FunctionProperty(
            script_command=self,
            property_name='app_dir_required',
            property_value=dir_required)

        self.function = app_dir_option(required=dir_required)(self.function)

        # Do not check if app is running
        FunctionProperty(
            script_command=self,
            property_name='app_should_run',
            property_value=should_run)

        # Say that the command is available ony in app context
        self.function.app_command = True

    def run_script(self, function, runner, script, variables: dict):
        kernel = runner.kernel
        manager = kernel.addons['app']

        if manager.app_dir:
            import os
            from dotenv import dotenv_values
            from addons.app.const.app import APP_FILEPATH_REL_DOCKER_ENV

            env_path = os.path.join(
                manager.app_dir,
                APP_FILEPATH_REL_DOCKER_ENV
            )

            app_variables = dotenv_values(env_path)
            if 'script' in script:
                script['script'] = string_replace_multiple(script['script'], app_variables)
            elif 'file' in script:
                script['file'] = string_replace_multiple(script['file'], app_variables)

            command = super().run_script(function, runner, script, variables)

            if 'container_name' in script:
                from src.helper.command import command_to_string
                command = command_to_string(command)
                command = command_escape(command)

                wrap_command = [
                    'docker',
                    'exec',
                    docker_build_long_container_name(kernel, script['container_name']),
                    SHELL_DEFAULT,
                    '-c',
                    command
                ]

                return wrap_command
        else:
            command = super().run_script(function, runner, script, variables)

        return command
