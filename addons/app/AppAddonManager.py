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
from src.helper.file import get_dict_item_by_path, write_dict_to_config, yaml_load_or_default, set_dict_item_by_path


class AppAddonManager(AddonManager):
    def __init__(self, kernel, name):
        super().__init__(kernel, name)
        self.call_command_level = None
        self.call_working_dir = os.getcwd()
        self.config = {}
        self.config_path = None
        self.proxy_apps = {}
        self.runtime_config = {}
        self.runtime_config_path = None

        if platform.system() == 'Darwin':
            self.proxy_path = '/Users/.wex/server/'
        else:
            self.proxy_path = '/opt/{}/'.format(PROXY_APP_NAME)

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
        self._save_yml_file(
            self.config_path,
            self.config
        )

    def _save_yml_file(self, path, config):
        self.log('Updating ' + path)

        with open(path, 'w') as file:
            yaml.safe_dump(config, file)

    def save_runtime_config(self):
        self._save_yml_file(
            self.runtime_config_path,
            self.runtime_config
        )

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

    @staticmethod
    def _set_config_value(config, key, value):
        # Avoid "#refs" in files
        if isinstance(value, dict) or isinstance(value, list):
            value = value.copy()

        set_dict_item_by_path(
            config,
            key,
            value
        )

    def set_config(self, key, value):
        self._set_config_value(
            self.config,
            key,
            value
        )

        self.save_config()

    def set_runtime_config(self, key, value):
        self._set_config_value(
            self.runtime_config,
            key,
            value
        )

        self.save_runtime_config()

    def get_config(self, key: str, default: None | int | str | bool = None) -> None | int | str | bool:
        return get_dict_item_by_path(self.config, key, default)

    def log(self, message: str, color=COLOR_GRAY, increment: int = 0) -> None:
        return self.kernel.log(
            f'[{self.name}] {message}',
            color,
            increment + 1
        )

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

        if self.call_command_level == -1:
            self.unset_app_workdir()

        elif self.call_command_level < -1:
            self.kernel.error(ERR_UNEXPECTED, {
                'error': 'More "post" execution than "pre" execution call'
            })

    def save_proxy_apps(self):
        with open(self.proxy_path + PROXY_FILE_APPS_REGISTRY, 'w') as f:
            yaml.dump(
                self.proxy_apps, f,
                indent=True
            )

    def set_app_workdir(self, app_dir: str = None):
        self.call_command_level = 0

        app_dir = self.kernel.exec_function(
            app__location__find, {
                'app-dir': app_dir
            }
        )

        if app_dir:
            os.chdir(app_dir)

            self.config_path = os.path.join(app_dir, APP_FILEPATH_REL_CONFIG)
            self.runtime_config_path = os.path.join(app_dir, APP_FILEPATH_REL_CONFIG_RUNTIME)
            self.config = self._load_config(self.config_path)

            self.proxy_apps = yaml_load_or_default(
                self.proxy_path + PROXY_FILE_APPS_REGISTRY,
                {}
            )

            self.runtime_config = self._load_config(
                self.runtime_config_path)

    def unset_app_workdir(self):
        self.call_command_level = None

        # Restore default working dir.
        os.chdir(self.call_working_dir)

    def exec_in_workdir(self, app_dir: str, callback):
        self.kernel.log_indent_up()
        app_dir_previous = os.getcwd() + '/'
        self.set_app_workdir(app_dir)

        response = callback()

        self.set_app_workdir(app_dir_previous)
        self.kernel.log_indent_down()

        return response
