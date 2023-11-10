import os
import platform
import datetime
import getpass
import yaml

from src.helper.args import args_shift_one, args_push_one
from src.helper.string import to_snake_case, to_kebab_case
from src.const.globals import COLOR_GRAY, VERBOSITY_LEVEL_MEDIUM, CORE_COMMAND_NAME, DATE_FORMAT_SECOND, \
    COMMAND_TYPE_APP
from src.core.AddonManager import AddonManager
from addons.app.const.app import APP_FILEPATH_REL_CONFIG, APP_FILEPATH_REL_CONFIG_RUNTIME, ERR_APP_NOT_FOUND, \
    PROXY_APP_NAME, APP_FILEPATH_REL_DOCKER_ENV, PROXY_FILE_APPS_REGISTRY, APP_FILEPATH_REL_COMPOSE_RUNTIME_YML, \
    APP_DIR_APP_DATA, ERR_APP_SHOULD_RUN, APP_ENV_TEST, APP_ENV_LOCAL, APP_ENV_DEV, APP_ENV_PROD, APP_FILEPATH_REL_ENV
from addons.app.command.location.find import app__location__find
from src.helper.file import write_dict_to_config, set_dict_item_by_path, env_to_dict
from src.helper.yaml import yaml_load_or_default
from src.helper.core import core_kernel_get_version
from src.helper.dict import get_dict_item_by_path


class AppAddonManager(AddonManager):
    def __init__(self, kernel, name: str = COMMAND_TYPE_APP, app_dir: None | str = None):
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

        if app_dir:
            self.set_app_workdir(app_dir)

        # Register extra decorators to allow using it in yaml scripts
        from addons.app.decorator.app_command import app_command
        from addons.app.decorator.app_webhook import app_webhook
        from addons.app.decorator.app_dir_option import app_dir_option
        from addons.app.decorator.option_webhook_listener import option_webhook_listener
        from addons.app.decorator.service_option import service_option

        self.kernel.decorators['command'].update({
            'app_command': app_command
        })

        self.kernel.decorators['extra'].update({
            'app_webhook': app_webhook,
            'app_dir_option': app_dir_option,
            'option_webhook_listener': option_webhook_listener,
            'service_option': service_option,
        })

    def get_applications_path(self) -> str:
        return os.sep + os.path.join('var', 'www', self.kernel.registry["env"]) + os.sep

    def get_env_file_path(self, file_relative_path: str, create: bool = False) -> str:
        relative_dir = os.path.dirname(
            file_relative_path
        )

        env_file_path = self.get_env_dir(relative_dir, create) + os.path.basename(file_relative_path)

        if create and not os.path.exists(env_file_path):
            with open(env_file_path, 'w'):
                pass

        return env_file_path

    def get_env_dir(self, dir: str, create: bool = False) -> str:
        if not self.app_dir:
            self.kernel.io.error('Trying to get env directory before setting working directory')

        env_dir = os.path.join(
            self.app_dir,
            APP_DIR_APP_DATA,
            dir
        ) + os.sep

        if create and not os.path.exists(env_dir):
            os.makedirs(env_dir, exist_ok=True)

        return env_dir

    def load_script(self, name: str) -> dict | None:
        script_dir = self.get_env_file_path(
            os.path.join(
                'script',
                name + '.yml'
            ))

        if not os.path.exists(script_dir):
            return None

        # Load the configuration file
        with open(script_dir, 'r') as file:
            return yaml.safe_load(file)

    def get_proxy_path(self) -> str:
        if platform.system() == 'Darwin':
            return os.sep + os.path.join('Users', '.wex', 'proxy') + os.sep
        else:
            return f'{self.get_applications_path()}{PROXY_APP_NAME}{os.sep}'

    def get_proxy_apps(self):
        return yaml_load_or_default(
            self.get_proxy_path() + PROXY_FILE_APPS_REGISTRY,
            {}
        )

    @classmethod
    def is_env_root(cls, app_dir: str) -> bool:
        if not os.path.exists(app_dir):
            return False

        # Search for config file.
        return os.path.exists(
            os.path.join(app_dir, APP_FILEPATH_REL_CONFIG)
        )

    @classmethod
    def is_app_root(cls, app_dir: str) -> bool:
        if cls.is_env_root(app_dir):
            config = cls._load_config(
                os.path.join(app_dir, APP_FILEPATH_REL_CONFIG)
            )

            return ('global' in config
                    and 'type' in config['global']
                    and config['global']['type'] == 'app')

    @classmethod
    def _load_config(cls, path, default: dict = {}):
        try:
            with open(path, 'r') as file:
                return yaml.safe_load(file)
        except Exception:
            return default

    def create_config(self, app_name: str, domains=None):
        if domains is None:
            domains = []

        domain_main = domains[0] if domains else f'{to_kebab_case(app_name)}.{CORE_COMMAND_NAME}'
        email = f'contact@{domain_main}'

        return {
            'global': {
                'author': getpass.getuser(),
                'created': datetime.datetime.utcnow().strftime(DATE_FORMAT_SECOND),
                'name': app_name,
                'services': [],
                'type': 'app'
            },
            'docker': {
                'compose': {
                    'tty': True,
                    'stdin_open': True,
                }
            },
            'env': {
                APP_ENV_TEST: {
                    'domains': domains.copy(),
                    'domain_main': domain_main,
                    'email': email
                },
                APP_ENV_LOCAL: {
                    'domains': domains.copy(),
                    'domain_main': domain_main,
                    'email': email
                },
                APP_ENV_DEV: {
                    'domains': domains.copy(),
                    'domain_main': domain_main,
                    'email': email
                },
                APP_ENV_PROD: {
                    'domains': domains.copy(),
                    'domain_main': domain_main,
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

        app_dir: str = self.get_runtime_config('path.app')

        app_env_path = os.path.join(
            app_dir,
            APP_FILEPATH_REL_ENV
        )

        env_dict = {
            '# .env config': True
        }

        env_dict.update(
            env_to_dict(app_env_path)
        )

        config_path = os.path.join(
            app_dir,
            APP_FILEPATH_REL_DOCKER_ENV
        )

        env_dict.update({
            '# Build config': True
        })

        env_dict.update(
            self.config_to_docker_env()
        )

        # Write as docker env file
        write_dict_to_config(
            env_dict,
            config_path
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

    def get_config(self, key: str, default: any = None, required: bool = False) -> any:
        value = get_dict_item_by_path(self.config, key, default)

        if required and value is None:
            self.kernel.io.error(
                f'Missing expected config key : {key}, got None',
                trace=False)

        return value

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

    def ignore_app_dir(self, request) -> bool:
        # Only specified commands will expect app location.
        if request.function_get_attr(
                name='app_command',
                default=False):
            return False
        return True

    def hook_render_request_pre(self, request):
        if self.ignore_app_dir(request):
            return

        args = request.args.copy()
        app_dir_arg = args_shift_one(args, 'app-dir')

        # User specified the app dir arg.
        if app_dir_arg is not None:
            app_dir_resolved = app_dir_arg
        else:
            # Previous app dir already exists.
            if self.app_dir is not None:
                app_dir_resolved = self.app_dir
            else:
                # Skip if the command allow to be executed without app location.
                if not request.function_get_attr(
                        name='app_dir_required',
                        default=False):
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

        args_push_one(
            arg_list=args,
            arg_name='app-dir',
            value=app_dir_resolved)

        if request.function_get_attr(
                name='app_should_run',
                default=False):
            from addons.app.command.app.started import app__app__started, APP_STARTED_CHECK_MODE_FULL

            if not self.kernel.run_function(app__app__started, {
                'app-dir': self.app_dir,
                'mode': APP_STARTED_CHECK_MODE_FULL
            }).first():
                import logging

                self.kernel.io.error(ERR_APP_SHOULD_RUN, {
                    'command': request.command,
                    'dir': app_dir_resolved,
                }, trace=False)

    def hook_render_request_post(self, response):
        if self.ignore_app_dir(response.request):
            return

        self.app_dirs_stack.pop()
        app_dir = self.app_dirs_stack[-1] if len(self.app_dirs_stack) else self.kernel.get_path('call')
        # Previous app dir was an app.
        if app_dir:
            # Reinit app dir if not the same.
            if app_dir != self.app_dir:
                self.set_app_workdir(app_dir)

    def add_proxy_app(self, name, app_dir):
        proxy_apps = self.get_proxy_apps()
        proxy_apps[name] = app_dir
        self.save_proxy_apps(proxy_apps)

    def save_proxy_apps(self, proxy_apps):
        with open(self.get_proxy_path() + PROXY_FILE_APPS_REGISTRY, 'w') as f:
            yaml.dump(
                proxy_apps, f,
                indent=True
            )

    def set_app_workdir(self, app_dir: str = None):
        self.app_dir = app_dir
        self.config_path = os.path.join(app_dir, APP_FILEPATH_REL_CONFIG)
        self.runtime_config_path = os.path.join(app_dir, APP_FILEPATH_REL_CONFIG_RUNTIME)
        self.runtime_docker_compose_path = os.path.join(app_dir, APP_FILEPATH_REL_COMPOSE_RUNTIME_YML)
        self.load_config()

        if os.getcwd() != app_dir.rstrip(os.sep):
            self.kernel.io.log(
                'Switching to app : ' + app_dir,
                verbosity=VERBOSITY_LEVEL_MEDIUM
            )

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

        if fallback_dir:
            # Print log in normal kernel.
            self.kernel.io.log(
                'Unset app dir to : ' + fallback_dir,
                verbosity=VERBOSITY_LEVEL_MEDIUM
            )

            os.chdir(fallback_dir)

    def exec_in_app_workdir(self, app_dir: str, callback):
        app_dir_previous = os.getcwd() + '/'
        self.set_app_workdir(app_dir)

        response = callback()

        self.set_app_workdir(app_dir_previous)

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
                'app_env': os.path.join(self.app_dir, APP_DIR_APP_DATA) + '/',
                'proxy': self.get_proxy_path()
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
        for service, service_data in self.kernel.registry['service'].items():
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


def _app__script__exec__create_callback(
        kernel,
        app_dir,
        command):
    def _callback(previous=None):
        from addons.app.command.app.exec import app__app__exec

        return kernel.run_function(
            app__app__exec,
            {
                'app-dir': app_dir,
                'command': command
            }
        )

    return _callback
