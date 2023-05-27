import os

from addons.app.command.location.find import app_location_find
from addons.app.const.app import ERR_APP_NOT_FOUND
from addons.app.helpers.app import set_app_workdir


def app_middleware_exec(kernel, *, addon=None, command=None, args=None, args_list=[], function, **kwargs) -> None:
    if addon == 'app':
        # Skip if the command allow to be executed without app location.
        if hasattr(function.callback, 'app_location_optional'):
            return

        if 'app-dir' in args:
            app_dir = args['app-dir']
            del args['app-dir']
        else:
            app_dir = os.getcwd()

        app_dir_resolved = kernel.exec_function(
            app_location_find,
            {
                'app-dir': app_dir
            }
        )

        if app_dir_resolved:
            # First test, create config.
            if not hasattr(kernel.addons['app']['config'], 'call_command_level'):
                set_app_workdir(kernel, app_dir_resolved)

                # Append to original apps list.
                args_list.append('--app-dir')
                args_list.append(app_dir_resolved)
            # Config exists.
            else:
                # Count deep level,
                # used to restore working dir when reverted to 0.
                kernel.addons['app']['config']['call_command_level'] += 1

        else:
            kernel.error(ERR_APP_NOT_FOUND, {
                'command': command,
                'dir': app_dir,
            })
