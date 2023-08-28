import os.path
import click

from addons.app.command.config.write import app__config__write
from addons.app.const.app import APP_FILEPATH_REL_ENV, APP_ENVS, APP_ENV_LOCAL, APP_FILEPATH_REL_COMPOSE_BUILD_YML
from addons.app.helpers.app import create_env, save_proxy_apps, config_save_build, app_exec_in_workdir
from addons.app.command.env.get import app__env__get
from addons.app.command.app.started import app__app__started
from addons.app.command.app.perms import app__app__perms
from addons.app.command.app.serve import app__app__serve
from addons.app.command.service.used import app__service__used
from addons.app.command.config.get import app__config__get
from addons.app.helpers.docker import exec_app_docker_compose
from addons.app.command.hook.exec import app__hook__exec
from src.helper.prompt import prompt_choice
from addons.app.helpers.app import app_log
from addons.app.decorator.app_dir_option import app_dir_option


@click.command()
@click.pass_obj
@app_dir_option()
@click.option(
    '--clear-cache', '-cc', is_flag=True, default=False,
    help="Forces a rebuild of images")
@click.option('--user', '-u', type=str, required=False,
              help="Owner of application files")
@click.option('--group', '-g', type=str, required=False,
              help="Group of application files")
@click.option('--env', '-e', type=str, required=False,
              help="App environment")
def app__app__start(kernel, app_dir: str, clear_cache: bool = False, user: str = None, group: str = None,
                    env: str = None):
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
                kernel.log('Abort')
                return

        create_env(env, app_dir)

        kernel.message(f'Created .env file for env "{env}"')
    else:
        env = app__env__get.callback(app_dir)

    if kernel.exec_function(app__app__started, {
        'app-dir': app_dir
    }):
        kernel.log('App already running')
        return

    name = app__config__get.callback(app_dir, 'global.name')
    proxy_path = kernel.addons['app']['path']['proxy']
    app_log(kernel, f"Starting app : {name}")

    # Current app is not the reverse proxy itself.
    if not kernel.exec_function(app__service__used, {'service': 'proxy', 'app-dir': app_dir}):
        # The reverse proxy is not running.
        if not kernel.exec_function(app__app__started, {'app-dir': proxy_path}):
            kernel.log('Starting proxy server')

            def start_proxy():
                from addons.app.command.proxy.start import app__proxy__start

                kernel.exec_function(
                    app__proxy__start,
                    {
                        'user': user,
                        'group': group,
                        'env': env,
                    }
                )

            app_exec_in_workdir(
                kernel,
                kernel.addons['app']['path']['proxy'],
                start_proxy
            )

    kernel.exec_function(
        app__app__perms,
        {
            'app-dir': app_dir
        }
    )

    kernel.exec_function(
        app__hook__exec,
        {
            'app-dir': app_dir,
            'hook': 'app/start-pre'
        }
    )

    kernel.exec_function(app__config__write, {
        'app-dir': app_dir,
        'user': user,
        'group': group,
    })

    # Save app in proxy apps.
    app_log(kernel, 'Registering app...')
    kernel.addons['app']['proxy']['apps'][name] = app_dir
    save_proxy_apps(kernel)

    compose_options = ['up', '-d']

    if clear_cache:
        compose_options.append('--build')

    service_results = kernel.exec_function(
        app__hook__exec,
        {
            'app-dir': app_dir,
            'hook': 'app/start-options',
            'arguments': {
                'options': compose_options
            }
        }
    )

    compose_options += [item for value in service_results.values() if isinstance(value, list) for item in value]

    # Start containers
    exec_app_docker_compose(
        kernel,
        [APP_FILEPATH_REL_COMPOSE_BUILD_YML],
        compose_options,
        sync=False
    )

    kernel.addons['app']['config_build']['context']['started'] = True
    config_save_build(
        kernel,
        app_dir
    )

    kernel.exec_function(
        app__hook__exec,
        {
            'app-dir': app_dir,
            'hook': 'app/start-post'
        }
    )

    kernel.exec_function(
        app__app__serve,
        {
            'app-dir': app_dir
        }
    )
