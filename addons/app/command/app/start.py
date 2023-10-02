import os.path
import click

from addons.app.command.config.write import app__config__write
from addons.app.const.app import APP_FILEPATH_REL_ENV, APP_ENVS, APP_ENV_LOCAL, APP_FILEPATH_REL_COMPOSE_RUNTIME_YML
from addons.app.command.env.get import app__env__get
from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.app.started import app__app__started, APP_STARTED_CHECK_MODE_FULL, \
    APP_STARTED_CHECK_MODE_ANY_CONTAINER
from addons.app.command.app.perms import app__app__perms
from addons.app.command.app.serve import app__app__serve
from addons.app.command.service.used import app__service__used
from addons.app.helpers.docker import exec_app_docker_compose
from addons.app.command.hook.exec import app__hook__exec
from src.core.response.ResponseCollectionStopResponse import ResponseCollectionStopResponse
from src.helper.process import process_post_exec_wex
from src.helper.prompt import prompt_choice
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.const.app import APP_FILEPATH_REL_ENV, APP_ENVS, APP_ENV_LOCAL
from addons.app.helpers.app import create_env
from src.helper.prompt import prompt_choice
from addons.app.helpers.app import create_env
from src.decorator.alias_without_addon import alias_without_addon
from src.decorator.command import command
from src.decorator.option import option
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse


@command(help="Start an app")
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
        if not kernel.run_function(app__service__used, {'service': 'proxy', 'app-dir': app_dir}):
            # The reverse proxy is not running.
            if not kernel.run_function(app__app__started, {
                'app-dir': manager.proxy_path,
                'mode': APP_STARTED_CHECK_MODE_ANY_CONTAINER
            }):
                manager.log('Starting proxy server')

                from addons.app.command.proxy.start import app__proxy__start

                kernel.run_function(
                    app__proxy__start,
                    {
                        'user': user,
                        'group': group,
                        'env': env,
                    }
                )

    def _app__app__start__app(previous):
        kernel.io.log(f"Starting app : {name}")

    # kernel.run_function(
    #     app__app__perms,
    #     {
    #         'app-dir': app_dir
    #     }
    # )
    #
    # kernel.run_function(
    #     app__hook__exec,
    #     {
    #         'app-dir': app_dir,
    #         'hook': 'app/start-pre'
    #     }
    # )
    #
    # kernel.run_function(
    #     app__config__write,
    #     {
    #         'app-dir': app_dir,
    #         'user': user,
    #         'group': group,
    #     })
    #
    # # Save app in proxy apps.
    # manager.log('Registering app...')
    # manager.proxy_apps[name] = app_dir
    # manager.save_proxy_apps()
    #
    # # Run docker compose
    # compose_options = ['up', '-d']
    #
    # if clear_cache:
    #     compose_options.append('--build')
    #
    # service_results = kernel.run_function(
    #     app__hook__exec,
    #     {
    #         'app-dir': app_dir,
    #         'hook': 'app/start-options',
    #         'arguments': {
    #             'app-dir': app_dir,
    #             'options': compose_options
    #         }
    #     }
    # ).first()
    #
    # compose_options += [item for value in service_results.values() if isinstance(value, list) for item in value]
    #
    # # Start containers
    # exec_app_docker_compose(
    #     kernel,
    #     app_dir,
    #     [APP_FILEPATH_REL_COMPOSE_RUNTIME_YML],
    #     compose_options,
    #     sync=False
    # )
    #
    # # TODO if build fails, app is still marked as started
    # #      We should create a queued steps system, to work with async bash scripts.
    # manager.set_runtime_config('started', True)
    #
    # # Postpone execution
    # process_post_exec_wex(
    #     kernel,
    #     app__hook__exec,
    #     {
    #         'app-dir': app_dir,
    #         'hook': 'app/start-post'
    #     }
    # )
    #
    # process_post_exec_wex(
    #     kernel,
    #     app__app__serve,
    #     {
    #         'app-dir': app_dir
    #     }
    # )

    return ResponseCollectionResponse(kernel, [
        _app__app__start__checkup,
        _app__app__start__proxy,
        _app__app__start__app,
    ])
