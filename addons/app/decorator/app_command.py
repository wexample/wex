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

        return function

    return decorator
