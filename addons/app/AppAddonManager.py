import os

import yaml

from src.const.globals import COLOR_GRAY
from src.const.error import ERR_UNEXPECTED
from src.core.AddonManager import AddonManager
from addons.app.const.app import APP_FILEPATH_REL_CONFIG, APP_FILEPATH_REL_CONFIG_RUNTIME, ERR_APP_NOT_FOUND
from addons.app.command.location.find import app__location__find
from src.helper.file import get_dict_item_by_path


class AppAddonManager(AddonManager):
    def __init__(self, kernel, name):
        super().__init__(kernel, name)
        self.config_path = None
        self.runtime_config_path = None
        self.call_command_level = None
        self.config = {}
        self.runtime_config = {}

    def load_current_app_configs(self):
        app_path = app__location__find.callback(
            os.getcwd()
        )

        if app_path:
            self.config_path = os.path.join(app_path, APP_FILEPATH_REL_CONFIG)
            self.runtime_config_path = os.path.join(app_path, APP_FILEPATH_REL_CONFIG_RUNTIME)
            self.config = self._load_config(self.config_path)
            self.runtime_config = self._load_config(self.runtime_config_path)

        pass

    @staticmethod
    def _load_config(path):
        try:
            with open(path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            return {}

    def save_config(self):
        with open(self.config_path, 'w') as file:
            yaml.safe_dump(self.config, file)

    def save_runtime_config(self):
        with open(self.runtime_config_path, 'w') as file:
            yaml.safe_dump(self.runtime_config, file)

    def update_config(self, key, value):
        self.config[key] = value
        self.save_config()

    def get_config(self, key: str) -> int | str | bool:
        return get_dict_item_by_path(self.config, key)

    def log(self, message: str, color=COLOR_GRAY, increment: int = 0) -> None:
        return self.kernel.log(
            f'[{self.name}] {message}',
            color,
            increment + 1
        )

    def update_runtime_config(self, key, value):
        self.runtime_config[key] = value
        self.save_runtime_config()

    def get_runtime_config(self, key: str, default: None | int | str | bool = None) -> None | int | str | bool:
        return get_dict_item_by_path(self.runtime_config, key, default)

    def command_exec_pre(self, function, args, command, args_list):
        # Skip if the command allow to be executed without app location.
        if hasattr(function.callback, 'app_location_optional'):
            return

        call_app_dir = self.get_runtime_config('path.call_app_dir')
        if call_app_dir is not None:
            app_dir_resolved = call_app_dir
        else:
            if 'app-dir' in args:
                app_dir = args['app-dir']
                del args['app-dir']
            else:
                app_dir = os.getcwd()

            app_dir_resolved = self.kernel.exec_function(
                app__location__find,
                {
                    'app-dir': app_dir
                }
            )

        if app_dir_resolved:
            args['app_dir'] = app_dir_resolved

            # First test, create config.
            if self.call_command_level is None:
                self.set_app_workdir(app_dir_resolved)
            # Config exists.
            else:
                # Count deep level,
                # used to restore working dir when reverted to 0.
                self.call_command_level += 1

            # Append to original apps list.
            args_list.append('--app-dir')
            args_list.append(app_dir_resolved)
        else:
            self.kernel.error(ERR_APP_NOT_FOUND, {
                'command': command,
                'dir': app_dir_resolved,
            })

    def command_exec_post(self, function):
        # Skip if the command allow to be executed without app location.
        if hasattr(function.callback, 'app_location_optional'):
            return

        self.call_command_level -= 1

        if self.call_command_level == 0:
            self.unset_app_workdir()

        elif self.call_command_level < 0:
            self.kernel.error(ERR_UNEXPECTED, {
                'error': 'More "post" execution than "pre" execution call'
            })

    def set_app_workdir(self, app_dir: str):
        self.call_command_level = 1

    def unset_app_workdir(self):
        self.call_command_level = None
