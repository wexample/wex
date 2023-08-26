import os.path
import click

from addons.app.command.config.write import app__config__write
from addons.app.const.app import APP_FILEPATH_REL_ENV, APP_ENVS, APP_ENV_LOCAL, APP_FILEPATH_REL_COMPOSE_BUILD_YML
from addons.app.helpers.app import create_env, set_app_workdir, save_proxy_apps
from addons.app.command.env.get import app__env__get
from addons.app.command.app.started import app__app__started
from addons.app.command.service.used import app__service__used
from addons.app.command.config.get import app__config__get
from addons.app.helpers.docker import exec_app_docker_compose
from addons.app.command.hook.exec import app__hook__exec
from src.helper.prompt import prompt_choice


@click.command()
@click.pass_obj
@click.option('--app-dir', '-a', type=str, required=True,
              help="App directory")
@click.option('--user', '-u', type=str, required=False,
              help="Owner of application files")
@click.option('--group', '-g', type=str, required=False,
              help="Group of application files")
@click.option('--env', '-e', type=str, required=False,
              help="App environment")
def app__app__start(kernel, app_dir: str = './', user: str = None, group: str = None, env: str = None):
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
        env = app__env__get.callback()

    if kernel.exec_function(app__app__started, {
        'app-dir': app_dir
    }):
        kernel.log('App already running')
        return

    name = app__config__get.callback('global.name')
    kernel.log(f"Starting app : {name}")

    proxy_path = kernel.addons['app']['path']['proxy']

    # Current app is not the reverse proxy itself.
    if not kernel.exec_function(app__service__used, {'service': 'proxy', 'app-dir': app_dir}):
        # The reverse proxy is not running.
        if not kernel.exec_function(app__app__started, {'app-dir': proxy_path}):
            app_start_proxy_and_retry(kernel, env, user, group)

    kernel.exec_function(app__config__write, {
        'app-dir': app_dir,
        'user': user,
        'group': group,
    })

    # Save app in proxy apps.
    kernel.log('Registering app')
    kernel.addons['app']['proxy']['apps'][name] = True
    save_proxy_apps(kernel)

    # Start containers
    exec_app_docker_compose(
        kernel,
        [APP_FILEPATH_REL_COMPOSE_BUILD_YML],
        ['up', '-d'],
        sync=False
    )

    kernel.exec_function(
        app__hook__exec,
        {
            'app-dir': app_dir,
            'hook': 'app/started'
        }
    )


def app_start_proxy_and_retry(kernel, env, user: str = None, group: str = None):
    from addons.app.command.proxy.start import app__proxy__start

    kernel.log('Starting proxy server')
    kernel.log_indent_up()
    app_dir = os.getcwd() + '/'

    kernel.exec_function(
        app__proxy__start,
        {
            'user': user,
            'group': group,
            'env': env,
        }
    )

    kernel.log_indent_down()
    # Reset current dir as app dir.
    set_app_workdir(kernel, app_dir)
