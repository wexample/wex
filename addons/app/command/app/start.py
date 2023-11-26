import os.path
import time
from typing import TYPE_CHECKING

import click

from addons.app.command.config.write import app__config__write
from addons.app.command.app.started import app__app__started, \
    APP_STARTED_CHECK_MODE_ANY_CONTAINER
from addons.app.command.app.perms import app__app__perms
from addons.app.command.app.serve import app__app__serve
from addons.app.command.service.used import app__service__used
from addons.app.helper.docker import docker_exec_app_compose_command
from addons.app.command.hook.exec import app__hook__exec
from addons.app.command.app.go import app__app__go
from addons.app.command.hosts.update import app__hosts__update
from src.const.globals import CORE_COMMAND_NAME
from src.core.response.HiddenResponse import HiddenResponse
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
from src.core.response.queue_collection.QueuedCollectionStopResponse import QueuedCollectionStopResponse
from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from addons.app.const.app import APP_FILEPATH_REL_ENV, APP_ENVS, APP_ENV_LOCAL, APP_FILEPATH_REL_COMPOSE_RUNTIME_YML, \
    APP_DIR_APP_DATA
from src.helper.prompt import prompt_choice
from addons.app.helper.app import app_create_env
from src.decorator.option import option
from src.decorator.as_sudo import as_sudo
from addons.app.decorator.app_command import app_command

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@as_sudo()
@app_command(help="Start an app")
@option(
    '--clear-cache', '-cc', is_flag=True, default=False,
    help="Forces a rebuild of images")
@option('--user', '-u', type=str, required=False,
        help="Owner of application files")
@option('--group', '-g', type=str, required=False,
        help="Group of application files")
@option('--env', '-e', type=str, required=False,
        help="App environment")
@option('--no-proxy', '-nopx', is_flag=True, required=False,
        help="Do not start proxy")
def app__app__start(
        manager: 'AppAddonManager',
        app_dir: str,
        clear_cache: bool = False,
        user: str = None,
        group: str = None,
        env: str = None,
        no_proxy: bool = False):
    kernel = manager.kernel
    name = manager.get_config('global.name')

    def _app__app__start__checkup():
        nonlocal env

        if not os.path.exists(APP_FILEPATH_REL_ENV):
            if not env:
                if click.confirm('No .wex/.env file, would you like to create it ?', default=True):
                    env = prompt_choice(
                        'Select an env:',
                        APP_ENVS,
                        APP_ENV_LOCAL
                    )

                # User said "no" or chose "abort"
                if not env:
                    manager.log('Abort')
                    return QueuedCollectionStopResponse(kernel)

            app_create_env(env, app_dir)

            kernel.io.message(f'Created .env file for env "{env}"')

        if kernel.run_function(app__app__started, {
            'app-dir': app_dir,
            'mode': APP_STARTED_CHECK_MODE_ANY_CONTAINER
        }).first():
            manager.log('App already running')
            return QueuedCollectionStopResponse(kernel, reason='APP_ALREADY_RUNNING')

    def _app__app__start__proxy(previous):
        if no_proxy:
            return

        # Current app is not the reverse proxy itself.
        if not kernel.run_function(app__service__used, {'service': 'proxy', 'app-dir': app_dir}).first():
            proxy_path = manager.get_proxy_path()

            # The reverse proxy is not running.
            if not os.path.exists(proxy_path) or not kernel.run_function(app__app__started, {
                'app-dir': proxy_path,
                'mode': APP_STARTED_CHECK_MODE_ANY_CONTAINER
            }).first():
                from addons.app.command.proxy.start import app__proxy__start
                return kernel.run_function(
                    app__proxy__start,
                    {
                        'user': user,
                        'group': group,
                        'env': env,
                    }
                )

    def _app__app__start__config(previous):
        kernel.run_function(
            app__app__perms,
            {
                'app-dir': app_dir
            }
        )

        kernel.run_function(
            app__hook__exec,
            {
                'app-dir': app_dir,
                'hook': 'app/start-pre'
            }
        )

        # Save app in proxy apps.
        manager.log('Registering app...')
        manager.add_proxy_app(name, app_dir)

        return kernel.run_function(
            app__config__write,
            {
                'app-dir': app_dir,
                'user': user,
                'group': group,
            })

    def _app__app__start__start_hooks(previous):
        # Run docker compose
        compose_options = ['up', '-d']

        if clear_cache:
            compose_options.append('--build')

        service_results = kernel.run_function(
            app__hook__exec,
            {
                'app-dir': app_dir,
                'hook': 'app/start-options',
                'arguments': {
                    'app-dir': app_dir,
                    'options': compose_options
                }
            }
        ).first()

        compose_options += [item for value in service_results.values() if isinstance(value, list) for item in value]

        return HiddenResponse(
            kernel,
            compose_options
        )

    def _app__app__start__starting(previous):
        return InteractiveShellCommandResponse(
            kernel,
            docker_exec_app_compose_command(
                kernel,
                app_dir,
                [APP_FILEPATH_REL_COMPOSE_RUNTIME_YML],
                previous,
            )
        )

    def _app__app__start__update_hosts(previous):
        manager.set_runtime_config('started', True)

        kernel.run_function(
            app__hosts__update
        )

    def _app__app__start__pending(previous):
        def _check():
            # Postpone execution
            response = kernel.run_function(
                app__hook__exec,
                {
                    'app-dir': app_dir,
                    'hook': 'service/ready'
                }
            )

            responses = response.first()
            for context in responses:
                if context and responses[context] and responses[context].first() == False:
                    kernel.io.log(f'@{context} is not running..')
                    return False

            return True

        while not _check():
            kernel.io.log(f'Waiting services..')
            time.sleep(2)

    def _app__app__start__serve(previous):
        # Postpone execution
        kernel.run_function(
            app__hook__exec,
            {
                'app-dir': app_dir,
                'hook': 'app/start-post'
            }
        )

        kernel.run_function(
            app__app__serve,
            {
                'app-dir': app_dir
            }
        )

    def _app__app__start__first_init(previous):
        env_dir = f'{manager.app_dir}{APP_DIR_APP_DATA}'
        first_start_lock = os.path.join(env_dir, 'tmp', f'{CORE_COMMAND_NAME}.first-start')
        if not os.path.exists(first_start_lock):
            kernel.run_function(
                app__hook__exec,
                {
                    'app-dir': app_dir,
                    'hook': 'app/first-init'
                }
            )

            with open(first_start_lock, 'w') as file:
                file.write('1')

            manager.set_runtime_config('initialized', True)

    def _app__app__start__complete(previous):
        env = manager.get_runtime_config('env')
        domains = manager.get_runtime_config('domains')
        domains_string = []

        for domain in domains:
            domains_string.append(f'- http{"s" if env != APP_ENV_LOCAL else ""}://{domain}')

        kernel.io.message(f'Your app is initialized as "{name}" in {env} environment',
                          os.linesep.join(domains_string))

        kernel.io.message_all_next_commands(
            [
                app__app__go,
            ]
        )

    return QueuedCollectionResponse(kernel, [
        _app__app__start__checkup,
        _app__app__start__proxy,
        _app__app__start__config,
        _app__app__start__start_hooks,
        _app__app__start__starting,
        _app__app__start__update_hosts,
        _app__app__start__pending,
        _app__app__start__serve,
        _app__app__start__first_init,
        _app__app__start__complete,
    ])
