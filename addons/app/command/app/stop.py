from __future__ import annotations

import click

from addons.app.const.app import APP_FILEPATH_REL_COMPOSE_RUNTIME_YML
from addons.app.command.app.started import app__app__started, APP_STARTED_CHECK_MODE_FULL
from addons.app.helpers.docker import exec_app_docker_compose
from addons.app.command.hook.exec import app__hook__exec
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel


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

    name = manager.name

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
        [APP_FILEPATH_REL_COMPOSE_RUNTIME_YML],
        ['down'],
        sync=False
    )

    manager.log('Unregistering app')
    if name in manager.proxy_apps:
        del manager.proxy_apps[name]
        manager.save_proxy_apps()

    # # TODO
    # # # Reload file
    # # # Rebuild hosts in wex registry.
    # # wex-exec app::hosts / update
    # # # Rebuild hosts global /etc/hosts.
    # # wex-exec app::hosts / updateLocal

    manager.set_runtime_config('started', False)

    kernel.exec_function(
        app__hook__exec,
        {
            'app-dir': app_dir,
            'hook': 'app/stop-post'
        }
    )
