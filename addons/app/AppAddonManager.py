import os
import platform

import yaml

from src.helper.string import to_snake_case
from src.const.globals import COLOR_GRAY
from src.const.error import ERR_UNEXPECTED
from src.core.AddonManager import AddonManager
from addons.app.const.app import APP_FILEPATH_REL_CONFIG, APP_FILEPATH_REL_CONFIG_RUNTIME, ERR_APP_NOT_FOUND, \
    PROXY_APP_NAME, APP_FILEPATH_REL_DOCKER_ENV, PROXY_FILE_APPS_REGISTRY
from addons.app.command.location.find import app__location__find
from src.helper.file import get_dict_item_by_path, write_dict_to_config, yaml_load_or_default


class AppAddonManager(AddonManager):
    def __init__(self, kernel, name):
        super().__init__(kernel, name)
        self.call_command_level = None
        self.config = {}
        self.config_path = None
        self.proxy_apps = {}
        self.proxy_path = None
        self.runtime_config = {}
        self.runtime_config_path = None

    def load_current_app_configs(self):
        app_path = self.kernel.exec_function(
            app__location__find
        )

        if app_path:
            self.config_path = os.path.join(app_path, APP_FILEPATH_REL_CONFIG)
            self.runtime_config_path = os.path.join(app_path, APP_FILEPATH_REL_CONFIG_RUNTIME)
            self.config = self._load_config(self.config_path)

            if platform.system() == 'Darwin':
                self.proxy_path = '/Users/.wex/server/'
            else:
                self.proxy_path = '/opt/{}/'.format(PROXY_APP_NAME)

            self.proxy_apps = yaml_load_or_default(
                self.proxy_path + PROXY_FILE_APPS_REGISTRY,
                {}
            )

            self.runtime_config = self._load_config(
                self.runtime_config_path,
                {
                    'path': {
                        'app': app_path,
                        'proxy': self.proxy_path
                    }
                }
            )

    @staticmethod
    def is_app_root(app_dir: str) -> bool:
        if not os.path.exists(app_dir):
            return False

        # Search for config file.
        return os.path.exists(
            os.path.join(app_dir, APP_FILEPATH_REL_CONFIG)
        )

    @staticmethod
    def _load_config(path, default: dict = {}):
        try:
            with open(path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            return default

    def save_config(self):
        with open(self.config_path, 'w') as file:
            yaml.safe_dump(self.config, file)

    def save_config_file(self):
        with open(self.config_path, 'w') as file:
            yaml.safe_dump(self.config, file)

    def save_runtime_config(self):
        # Build yml
        with open(self.runtime_config_path, 'w') as file:
            yaml.safe_dump(self.runtime_config, file)

        # Write as docker env file
        write_dict_to_config(
            self.config_to_docker_env(),
            os.path.join(
                self.get_runtime_config('path.app'),
                APP_FILEPATH_REL_DOCKER_ENV
            )
        )

    def config_to_docker_env(self):
        return self.dict_to_docker_env(
            dict(
                sorted(
                    self.runtime_config.items()
                )
            )
        )

    def dict_to_docker_env(self, config, parent_key='', sep='_'):
        items = []

        for k, v in config.items():
            new_key = parent_key + sep + k if parent_key else k
            new_key = to_snake_case(new_key)
            new_key = new_key.upper()
            if isinstance(v, dict):
                items.extend(self.dict_to_docker_env(
                    v,
                    new_key,
                    sep=sep
                ).items())
            else:
                items.append((new_key, v))
        return dict(items)

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

    def save_proxy_apps(self):
        with open(self.proxy_path + PROXY_FILE_APPS_REGISTRY, 'w') as f:
            yaml.dump(
                self.proxy_apps, f,
                indent=True
            )

    def set_app_workdir(self, app_dir: str):
        self.call_command_level = 1

    def unset_app_workdir(self):
        self.call_command_level = None
