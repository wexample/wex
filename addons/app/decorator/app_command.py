from addons.app.helpers.docker import build_long_container_name
from src.decorator.command import command
from addons.app.decorator.app_dir_option import app_dir_option


def app_command(**decorator_args):
    def decorator(function):
        # Say that the command is available ony in app context
        function.app_command = True

        # Do not provide app_dir to function
        function.app_dir_required = decorator_args.pop('dir_required', True)
        function = app_dir_option(
            required=function.app_dir_required
        )(function)

        # Do not check if app is running
        function.app_should_run = decorator_args.pop('should_run', False)

        function = command(**decorator_args)(function)

        # Override base handler
        function.base_run_handler = function.run_handler
        function.base_script_run_handler = function.script_run_handler
        function.run_handler = _app_run_handler
        function.script_run_handler = _app_script_run_handler

        return function

    return decorator


def _app_run_handler(runner, function, ctx):
    return function.base_run_handler(runner, function, ctx)


def _app_script_run_handler(function, runner, script, env_args: dict):
    kernel = runner.kernel
    manager = kernel.addons['app']
    command = function.base_script_run_handler(function, runner, script, env_args)

    if manager.app_dir:
        import os
        from dotenv import dotenv_values
        from addons.app.const.app import APP_FILEPATH_REL_DOCKER_ENV

        env_path = os.path.join(
            manager.app_dir,
            APP_FILEPATH_REL_DOCKER_ENV
        )

        if os.path.exists(env_path):
            env_args.update(
                dotenv_values(env_path)
            )

        if 'container_name' in script:
            from src.helper.command import command_to_string

            wrap_command = [
                'docker',
                'exec',
                build_long_container_name(kernel, script['container_name']),
                '/bin/bash',
                '-c',
                command_to_string(command)
            ]

            return wrap_command

    return command
