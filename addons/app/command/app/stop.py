import click

from addons.app.const.app import APP_FILEPATH_REL_COMPOSE_BUILD_YML
from addons.app.helpers.app import save_proxy_apps, config_save_build
from addons.app.command.app.started import app__app__started, APP_STARTED_CHECK_MODE_FULL
from addons.app.command.config.get import app__config__get
from addons.app.helpers.docker import exec_app_docker_compose
from addons.app.command.hook.exec import app__hook__exec
from addons.app.helpers.app import app_log
from addons.app.decorator.app_dir_option import app_dir_option


@click.command()
@click.pass_obj
@app_dir_option()
def app__app__stop(kernel: 'Kernel', app_dir: str):
    manager: 'AppAddonManager' = kernel.addons['app']

    if not kernel.exec_function(app__app__started, {
        'app-dir': app_dir,
        'check-mode': APP_STARTED_CHECK_MODE_FULL
    }):
        manager.log('App already stopped')
        return

    name = app__config__get.callback(app_dir, 'global.name')

    kernel.exec_function(
        app__hook__exec,
        {
            'app-dir': app_dir,
            'hook': 'app/stop-pre'
        }
    )

    # Stop containers
    exec_app_docker_compose(
        kernel,
        app_dir,
        [APP_FILEPATH_REL_COMPOSE_BUILD_YML],
        ['down'],
        sync=False
    )

    app_log(kernel, 'Unregistering app')
    del kernel.addons['app']['proxy']['apps'][name]
    save_proxy_apps(kernel)

    # TODO
    # # Reload file
    # # Rebuild hosts in wex registry.
    # wex-exec app::hosts / update
    # # Rebuild hosts global /etc/hosts.
    # wex-exec app::hosts / updateLocal

    kernel.addons['app']['config_build']['context']['started'] = False
    config_save_build(
        kernel,
        app_dir
    )

    kernel.exec_function(
        app__hook__exec,
        {
            'app-dir': app_dir,
            'hook': 'app/stop-post'
        }
    )
