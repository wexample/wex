from addons.app.helper.docker import build_long_container_name
from src.helper.command import command_escape
from src.helper.string import replace_variables
from src.const.globals import SHELL_DEFAULT
from src.decorator.command import command
from src.core.FunctionProperty import FunctionProperty
from addons.app.decorator.app_dir_option import app_dir_option


def app_command(**decorator_args):
    def decorator(function):
        # Get and pop interesting args
        dir_required = decorator_args.pop('dir_required', True)
        should_run = decorator_args.pop('should_run', False)

        # Convert function to command
        function = command(**decorator_args)(function)

        # Do not provide app_dir to function
        FunctionProperty(
            function=function,
            property_name='app_dir_required',
            property_value=dir_required)

        function = app_dir_option(required=dir_required)(function)

        # Do not check if app is running
        FunctionProperty(
            function=function,
            property_name='app_should_run',
            property_value=should_run)

        # Say that the command is available ony in app context
        function.app_command = True

        # Override base handler
        function.base_run_handler = function.run_handler
        function.base_script_run_handler = function.script_run_handler
        function.run_handler = _app_run_handler
        function.script_run_handler = _app_script_run_handler

        return function

    return decorator


def _app_run_handler(runner, function, ctx):
    return function.base_run_handler(runner, function, ctx)


def _app_script_run_handler(function, runner, script, variables: dict):
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
            script['script'] = replace_variables(script['script'], app_variables)
        elif 'file' in script:
            script['file'] = replace_variables(script['file'], app_variables)

        command = function.base_script_run_handler(function, runner, script, variables)

        if 'container_name' in script:
            from src.helper.command import command_to_string
            command = command_to_string(command)
            command = command_escape(command)

            wrap_command = [
                'docker',
                'exec',
                build_long_container_name(kernel, script['container_name']),
                SHELL_DEFAULT,
                '-c',
                command
            ]

            return wrap_command
    else:
        command = function.base_script_run_handler(function, runner, script, variables)

    return command
