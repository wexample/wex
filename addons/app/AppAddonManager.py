import os
import platform
import datetime
import getpass
import yaml

from src.helper.args import arg_shift, arg_push
from src.helper.string import to_snake_case, to_kebab_case
from src.const.globals import COLOR_GRAY, VERBOSITY_LEVEL_MEDIUM
from src.core.AddonManager import AddonManager
from addons.app.const.app import APP_FILEPATH_REL_CONFIG, APP_FILEPATH_REL_CONFIG_RUNTIME, ERR_APP_NOT_FOUND, \
    PROXY_APP_NAME, APP_FILEPATH_REL_DOCKER_ENV, PROXY_FILE_APPS_REGISTRY, APP_FILEPATH_REL_COMPOSE_RUNTIME_YML
from addons.app.command.location.find import app__location__find
from src.helper.file import write_dict_to_config, yaml_load_or_default, set_dict_item_by_path
from src.helper.core import core_kernel_get_version
from src.helper.dict import get_dict_item_by_path


class AppAddonManager(AddonManager):
    def __init__(self, kernel, name):
        super().__init__(kernel, name)
        self.call_working_dir = os.getcwd() + os.sep
        self.app_dir = None
        self.config = {}
        self.config_path = None
        self.proxy_apps = {}
        self.runtime_config = {}
        self.runtime_config_path = None
        self.runtime_docker_compose = None
        self.runtime_docker_compose_path = None

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
        except Exception:
            return default

    def create_config(self, app_name: str, domains=None):
        if domains is None:
            domains = []

        domains_main = domains[0] if domains else f'{to_kebab_case(app_name)}.wex'
        email = f'contact@{domains_main}'

        return {
            'global': {
                'author': getpass.getuser(),
                'created': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                'name': app_name,
                'services': [],
            },
            'docker': {
                'compose': {
                    'tty': True,
                    'stdin_open': True,
                }
            },
            'env': {
                'local': {
                    'domains': f'{app_name}.wex',
                    'domain_main': f'{app_name}.wex',
                    'email': email
                },
                'dev': {
                    'domains': domains.copy(),
                    'domain_main': domains_main,
                    'email': email
                },
                'prod': {
                    'domains': domains.copy(),
                    'domain_main': domains_main,
                    'email': email
                }
            },
            'wex': {
                'version': core_kernel_get_version(self.kernel)
            }
        }

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
        config = self.config.copy()
        config['runtime'] = dict(
            sorted(
                self.runtime_config.items()
            )
        )
        return self.dict_to_docker_env(config)

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
    def _set_config_value(config, key, value, replace: bool = True):
        # Avoid "#refs" in files
        if isinstance(value, dict) or isinstance(value, list):
            value = value.copy()

        set_dict_item_by_path(
            config,
            key,
            value,
            replace
        )

    def set_config(self, key, value, replace: bool = True):
        self._set_config_value(
            self.config,
            key,
            value,
            replace
        )

        self.save_config()

    def set_runtime_config(self, key, value, replace: bool = True):
        self._set_config_value(
            self.runtime_config,
            key,
            value,
            replace
        )

        self.save_runtime_config()

    def get_config(self, key: str, default: any = None) -> any:
        return get_dict_item_by_path(self.config, key, default)

    def log(self, message: str, color=COLOR_GRAY, increment: int = 0) -> None:
        return self.kernel.io.log(
            f'[{self.get_config("global.name")}] {message}',
            color,
            increment + 1
        )

    def get_runtime_config(self, key: str, default: None | int | str | bool = None) -> None | int | str | bool:
        return get_dict_item_by_path(self.runtime_config, key, default)

    def command_run_pre(self, request):
        # Skip if the command allow to be executed without app location.
        if hasattr(request.function.callback, 'app_dir_ignore'):
            return

        if request.is_click_command(app__location__find):
            return

        args = request.args.copy()
        app_dir_arg = arg_shift(args, 'app-dir')
        app_dir_resolved = None

        if app_dir_arg is not None:
            app_dir_resolved = app_dir_arg
        else:
            if self.app_dir is not None:
                app_dir_resolved = self.app_dir
            else:
                # Skip if the command allow to be executed without app location.
                if hasattr(request.function.callback, 'app_dir_optional'):
                    return

                app_dir = os.getcwd() + os.sep

                app_dir_resolved = self.kernel.run_function(
                    app__location__find,
                    {
                        'app-dir': app_dir
                    }
                ).first()

        if app_dir_resolved:
            # Ensure it always ends with a /
            if not app_dir_resolved.endswith(os.sep):
                app_dir_resolved += os.sep

            # First test, create config.
            if 'previous_app_dir' not in request.storage:
                dirs_differ = os.path.realpath(app_dir_resolved) != os.path.realpath(os.getcwd())

                if dirs_differ or self.app_dir is None:
                    self.set_app_workdir(app_dir_resolved)

                if dirs_differ:
                    request.storage['previous_app_dir'] = app_dir_resolved

            # Append to original apps list.
            request.args = args
            arg_push(
                args,
                'app-dir',
                app_dir_resolved)
        else:
            import logging

            self.kernel.io.error(ERR_APP_NOT_FOUND, {
                'command': request.command,
                'dir': app_dir_resolved,
            }, logging.ERROR)

            exit(0)

    def command_run_post(self, request):
        if 'previous_app_dir' in request.storage:
            self.unset_app_workdir(request.storage['previous_app_dir'])
            del request.storage['previous_app_dir']

    def save_proxy_apps(self):
        with open(self.proxy_path + PROXY_FILE_APPS_REGISTRY, 'w') as f:
            yaml.dump(
                self.proxy_apps, f,
                indent=True
            )

    def set_app_workdir(self, app_dir: str = None):
        self.kernel.io.log(
            'Switching to app : ' + app_dir,
            verbosity=VERBOSITY_LEVEL_MEDIUM
        )

        self.app_dir = app_dir
        self.config_path = os.path.join(app_dir, APP_FILEPATH_REL_CONFIG)
        self.runtime_config_path = os.path.join(app_dir, APP_FILEPATH_REL_CONFIG_RUNTIME)
        self.runtime_docker_compose_path = os.path.join(app_dir, APP_FILEPATH_REL_COMPOSE_RUNTIME_YML)
        self.config = self._load_config(self.config_path)

        self.proxy_apps = yaml_load_or_default(
            self.proxy_path + PROXY_FILE_APPS_REGISTRY,
            {}
        )

        self.runtime_config = self._load_config(
            self.runtime_config_path)

        self.runtime_docker_compose = self._load_config(
            self.runtime_docker_compose_path)

        os.chdir(app_dir)

    def unset_app_workdir(self, fallback_dir: str):
        self.app_dir = None

        os.chdir(fallback_dir)

        # Print log in normal kernel.
        self.kernel.io.log('Switching to default : ' + self.call_working_dir)

    def exec_in_workdir(self, app_dir: str, callback):
        self.kernel.io.log_indent_up()
        app_dir_previous = os.getcwd() + '/'
        self.set_app_workdir(app_dir)

        response = callback()

        self.set_app_workdir(app_dir_previous)
        self.kernel.io.log_indent_down()

        return response
