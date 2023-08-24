import os

from addons.app.command.location.find import app__location__find
from addons.app.const.app import ERR_APP_NOT_FOUND
from addons.app.helpers.app import set_app_workdir
from src.const.globals import COMMAND_TYPE_ADDON


def app_middleware_exec(kernel, *, match=None, command=None, command_type: str = None, args=None, args_list=[],
                        function, **kwargs) -> None:
    if command_type == COMMAND_TYPE_ADDON:
        addon, group, name = match.groups()

        if addon == 'app':
            # Skip if the command allow to be executed without app location.
            if hasattr(function.callback, 'app_location_optional'):
                return

            if 'call_app_dir' in kernel.addons['app']['config']:
                app_dir_resolved = kernel.addons['app']['path']['call_app_dir']
            else:
                if 'app-dir' in args:
                    app_dir = args['app-dir']
                    del args['app-dir']
                else:
                    app_dir = os.getcwd()

                app_dir_resolved = kernel.exec_function(
                    app__location__find,
                    {
                        'app-dir': app_dir
                    }
                )

            if app_dir_resolved:
                args['app_dir'] = app_dir_resolved

                # First test, create config.
                if 'call_command_level' not in kernel.addons['app']:
                    set_app_workdir(kernel, app_dir_resolved)
                # Config exists.
                else:
                    # Count deep level,
                    # used to restore working dir when reverted to 0.
                    kernel.addons['app']['call_command_level'] += 1

                # Append to original apps list.
                args_list.append('--app-dir')
                args_list.append(app_dir_resolved)
            else:
                kernel.error(ERR_APP_NOT_FOUND, {
                    'command': command,
                    'dir': app_dir_resolved,
                })
