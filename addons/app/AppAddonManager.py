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
    PROXY_APP_NAME, APP_FILEPATH_REL_DOCKER_ENV, PROXY_FILE_APPS_REGISTRY, APP_FILEPATH_REL_COMPOSE_RUNTIME_YML, \
    APP_DIR_APP_DATA, ERR_APP_SHOULD_RUN, APP_ENV_TEST, APP_ENV_LOCAL, APP_ENV_DEV, APP_ENV_PROD
from addons.app.command.location.find import app__location__find
from src.helper.file import write_dict_to_config, yaml_load_or_default, set_dict_item_by_path
from src.helper.core import core_kernel_get_version
from src.helper.dict import get_dict_item_by_path


class AppAddonManager(AddonManager):
    def __init__(self, kernel, name):
        super().__init__(kernel, name)
        self.app_dir = None
        self.config = {}
        self.config_path = None
        self.app_dirs_stack = []
        self.runtime_config = {}
        self.runtime_config_path = None
        self.runtime_docker_compose = None
        self.runtime_docker_compose_path = None
        self.first_log_indent = None

        if platform.system() == 'Darwin':
            self.proxy_path = '/Users/.wex/server/'
        else:
            self.proxy_path = '/opt/{}/'.format(PROXY_APP_NAME)

        self.proxy_apps = yaml_load_or_default(
            self.proxy_path + PROXY_FILE_APPS_REGISTRY,
            {}
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
                APP_ENV_TEST: {
                    'domains': f'{app_name}.test',
                    'domain_main': f'{app_name}.test',
                    'email': email
                },
                APP_ENV_LOCAL: {
                    'domains': f'{app_name}.wex',
                    'domain_main': f'{app_name}.wex',
                    'email': email
                },
                APP_ENV_DEV: {
                    'domains': domains.copy(),
                    'domain_main': domains_main,
                    'email': email
                },
                APP_ENV_PROD: {
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

    def log(self, message: str, color=COLOR_GRAY, indent: int = 0) -> None:
        if self.first_log_indent is None:
            self.first_log_indent = self.kernel.io.log_indent

        if self.kernel.io.log_indent == self.first_log_indent:
            message = f'[{self.get_config("global.name")}] {message}'

        return self.kernel.io.log(
            message,
            color,
            indent
        )

    def get_runtime_config(self, key: str, default: None | int | str | bool = None) -> None | int | str | bool:
        return get_dict_item_by_path(self.runtime_config, key, default)

    def skip_app_location(self, request) -> bool:
        # Skip if the command allow to be executed without app location.
        if hasattr(request.function.callback, 'app_dir_ignore'):
            return True

        if request.is_click_command(app__location__find):
            return True

        return False

    def command_run_pre(self, request):
        if self.skip_app_location(request):
            return

        args = request.args.copy()
        app_dir_arg = arg_shift(args, 'app-dir')

        # User specified the app dir arg.
        if app_dir_arg is not None:
            app_dir_resolved = app_dir_arg
        else:
            # Previous app dir already exists.
            if self.app_dir is not None:
                app_dir_resolved = self.app_dir
            else:
                # Skip if the command allow to be executed without app location.
                if hasattr(request.function.callback, 'app_dir_optional'):
                    self.app_dirs_stack.append(None)
                    self.unset_app_workdir()
                    return

                app_dir = os.getcwd() + os.sep

                app_dir_resolved = self.kernel.run_function(
                    app__location__find,
                    {
                        'app-dir': app_dir
                    }
                ).first()

        if not app_dir_resolved:
            import logging

            self.kernel.io.error(ERR_APP_NOT_FOUND, {
                'command': request.command,
                'dir': app_dir_resolved,
            }, logging.ERROR)

            exit(0)

        # Ensure it always ends with a /
        if not app_dir_resolved.endswith(os.sep):
            app_dir_resolved += os.sep

        # First test, create config.
        if self.app_dir != app_dir_resolved:
            self.set_app_workdir(app_dir_resolved)

        self.app_dirs_stack.append(app_dir_resolved)

        # Append to original apps list.
        request.args = args
        arg_push(
            args,
            'app-dir',
            app_dir_resolved)

        if hasattr(request.function.callback, 'app_should_run'):
            from addons.app.command.app.started import app__app__started, APP_STARTED_CHECK_MODE_FULL

            if not self.kernel.run_function(app__app__started, {
                'app-dir': self.app_dir,
                'mode': APP_STARTED_CHECK_MODE_FULL
            }).first():
                import logging

                self.kernel.io.error(ERR_APP_SHOULD_RUN, {
                    'command': request.command,
                    'dir': app_dir_resolved,
                }, logging.ERROR)

                exit(0)

    def command_run_post(self, request):
        if self.skip_app_location(request):
            return

        self.app_dirs_stack.pop()
        app_dir = self.app_dirs_stack[-1] if len(self.app_dirs_stack) else None
        # Previous app dir was an app.
        if app_dir:
            # Reinit app dir if not the same.
            if app_dir != self.app_dir:
                self.set_app_workdir(app_dir)
        else:
            self.unset_app_workdir(
                app_dir
            )

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

        self.load_config()

        os.chdir(app_dir)

    def load_config(self):
        self.config = self._load_config(self.config_path)

        self.runtime_config = self._load_config(
            self.runtime_config_path)

        self.runtime_docker_compose = self._load_config(
            self.runtime_docker_compose_path)

    def unset_app_workdir(self, fallback_dir: str | None = None):
        self.app_dir = None
        self.config_path = None
        self.runtime_config_path = None
        self.runtime_docker_compose_path = None
        self.config = None
        self.runtime_config = None
        self.runtime_docker_compose = None

        fallback_dir = fallback_dir or self.kernel.path['call']
        os.chdir(fallback_dir)

        # Print log in normal kernel.
        self.kernel.io.log(
            'Unset app dir to : ' + fallback_dir,
            verbosity=VERBOSITY_LEVEL_MEDIUM
        )

    def exec_in_app_workdir(self, app_dir: str, callback):
        self.kernel.io.log_indent_up()
        app_dir_previous = os.getcwd() + '/'
        self.set_app_workdir(app_dir)

        response = callback()

        self.set_app_workdir(app_dir_previous)
        self.kernel.io.log_indent_down()

        return response

    def build_runtime_config(self, user: str = None, group: str = None):
        import socket
        from addons.app.command.env.get import app__env__get
        from src.const.globals import PASSWORD_INSECURE
        from src.helper.system import get_gid_from_group_name, \
            get_uid_from_user_name
        from src.helper.system import get_user_or_sudo_user, get_user_group_name
        from addons.app.command.hook.exec import app__hook__exec

        env = self.kernel.run_function(app__env__get, {'app-dir': self.app_dir}).first()
        user = user or get_user_or_sudo_user()
        group = group or get_user_group_name(user)
        name = self.get_config('global.name')

        self.log(f'Using user {user}:{group}')

        # Get a full config copy
        runtime_config = self.config.copy()
        # Add the per-environment config.
        runtime_config.update(self.config['env'][env])

        domains = []
        if 'domains' in runtime_config:
            domains = runtime_config['domains']

        if 'domain_main' in runtime_config and runtime_config['domain_main'] not in domains:
            domains.append(runtime_config['domain_main'])

        # Add extra runtime config.
        runtime_config.update({
            'domains': domains,
            'domains_string': ','.join(domains),
            'domain_tld': (runtime_config['domain_tld']
                           if 'domain_tld' in runtime_config
                           else runtime_config['domain_main']),
            'env': env,
            'name': f'{name}_{env}',
            'host': {
                'ip': socket.gethostbyname(
                    socket.gethostname()
                )
            },
            'password': {
                'insecure': PASSWORD_INSECURE
            },
            'path': {
                'app': self.app_dir,
                'app_wex': os.path.join(self.app_dir, APP_DIR_APP_DATA) + '/',
                'proxy': self.proxy_path
            },
            'service': {},
            'started': False,
            'user': {
                'group': group,
                'gid': get_gid_from_group_name(group),
                'name': user,
                'uid': get_uid_from_user_name(user),
            }
        })

        # Build paths to services docker compose yml files.
        for service, service_data in self.kernel.registry['services'].items():
            base_yml = service_data['dir'] + 'docker/docker-compose.yml'
            env_yml = service_data['dir'] + f'docker/docker-compose.{env}.yml'

            if not os.path.exists(env_yml):
                env_yml = base_yml

            runtime_config['service'][service] = {
                'yml': {
                    'base': base_yml,
                    'env': env_yml,
                }
            }

        self.log(f'Build config file')

        self.runtime_config = runtime_config
        self.save_runtime_config()

        self.kernel.run_function(
            app__hook__exec,
            {
                'app-dir': self.app_dir,
                'hook': 'config/runtime'
            }
        )

    def run_app_function(self, function: callable, args: dict):
        args['app-dir'] = self.app_dir

        return self.kernel.run_function(
            function,
            args
        )
