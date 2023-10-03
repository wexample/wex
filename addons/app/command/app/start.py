import os.path
import click

from addons.app.command.config.write import app__config__write
from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.app.started import app__app__started, \
    APP_STARTED_CHECK_MODE_ANY_CONTAINER
from addons.app.command.app.perms import app__app__perms
from addons.app.command.app.serve import app__app__serve
from addons.app.command.service.used import app__service__used
from addons.app.helpers.docker import exec_app_docker_compose_command
from addons.app.command.hook.exec import app__hook__exec
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.core.response.ResponseCollectionStopResponse import ResponseCollectionStopResponse
from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.const.app import APP_FILEPATH_REL_ENV, APP_ENVS, APP_ENV_LOCAL, APP_FILEPATH_REL_COMPOSE_RUNTIME_YML
from src.helper.prompt import prompt_choice
from addons.app.helpers.app import create_env
from src.decorator.alias_without_addon import alias_without_addon
from src.decorator.command import command
from src.decorator.option import option
from src.decorator.as_sudo import as_sudo


@command(help="Start an app")
@as_sudo
@alias_without_addon()
@app_dir_option()
@option(
    '--clear-cache', '-cc', is_flag=True, default=False,
    help="Forces a rebuild of images")
@option('--user', '-u', type=str, required=False,
        help="Owner of application files")
@option('--group', '-g', type=str, required=False,
        help="Group of application files")
@option('--env', '-e', type=str, required=False,
        help="App environment")
def app__app__start(
        kernel,
        app_dir: str,
        clear_cache: bool = False,
        user: str = None,
        group: str = None,
        env: str = None):
    manager: AppAddonManager = kernel.addons['app']
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
                    return

            create_env(env, app_dir)

            kernel.io.message(f'Created .env file for env "{env}"')

        if kernel.run_function(app__app__started, {
            'app-dir': app_dir,
            'mode': APP_STARTED_CHECK_MODE_ANY_CONTAINER
        }).first():
            manager.log('App already running')
            return ResponseCollectionStopResponse(kernel)

    def _app__app__start__proxy(previous):
        # Current app is not the reverse proxy itself.
        if not kernel.run_function(app__service__used, {'service': 'proxy', 'app-dir': app_dir}).first():
            # The reverse proxy is not running.
            if not kernel.run_function(app__app__started, {
                'app-dir': manager.proxy_path,
                'mode': APP_STARTED_CHECK_MODE_ANY_CONTAINER
            }).first():
                from addons.app.command.proxy.start import app__proxy__start

                kernel.run_function(
                    app__proxy__start,
                    {
                        'user': user,
                        'group': group,
                        'env': env,
                    }
                )

                return

    def _app__app__start__config(previous):
        manager.log(f"Starting app : {name}")

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
        manager.proxy_apps[name] = app_dir
        manager.save_proxy_apps()

        return kernel.run_function(
            app__config__write,
            {
                'app-dir': app_dir,
                'user': user,
                'group': group,
            })

    def _app__app__start__starting(previous):
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

        # TODO Return directly InteractiveShellCommandResponse when working.
        return ResponseCollectionResponse(kernel, [
            InteractiveShellCommandResponse(
                kernel,
                exec_app_docker_compose_command(
                    kernel,
                    app_dir,
                    [APP_FILEPATH_REL_COMPOSE_RUNTIME_YML],
                    compose_options,
                    sync=False
                )
            )
        ])

    def _app__app__start__complete(previous):
        manager.set_runtime_config('started', True)

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

    return ResponseCollectionResponse(kernel, [
        _app__app__start__checkup,
        _app__app__start__proxy,
        _app__app__start__config,
        _app__app__start__starting,
        _app__app__start__complete,
    ])
