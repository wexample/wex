from typing import TYPE_CHECKING

from addons.app.command.app.perms import app__app__perms
from addons.app.command.app.started import app__app__started
from addons.app.command.hook.exec import app__hook__exec
from addons.app.command.hosts.update import app__hosts__update
from addons.app.const.app import APP_FILEPATH_REL_COMPOSE_RUNTIME_YML
from addons.app.decorator.app_command import app_command
from addons.app.helper.docker import docker_exec_app_compose_command
from src.core.response.InteractiveShellCommandResponse import \
    InteractiveShellCommandResponse
from src.core.response.queue_collection.QueuedCollectionStopResponse import \
    QueuedCollectionStopResponse
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
from src.decorator.as_sudo import as_sudo

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@as_sudo()
@app_command(help="Stop the given app")
def app__app__stop(manager: 'AppAddonManager', app_dir: str):
    kernel = manager.kernel
    name = manager.get_config('global.name')

    def _app__app__stop__checkup():
        if not kernel.run_function(app__app__started, {
            'app-dir': app_dir
        }).first():
            manager.log('App already stopped')
            return QueuedCollectionStopResponse(kernel)

        kernel.run_function(
            app__app__perms,
            {
                'app-dir': app_dir
            }
        )

    def _app__app__stop__stop(previous):
        kernel.run_function(
            app__hook__exec,
            {
                'app-dir': app_dir,
                'hook': 'app/stop-pre'
            }
        )

        return QueuedCollectionResponse(kernel, [
            InteractiveShellCommandResponse(
                kernel,
                docker_exec_app_compose_command(
                    kernel,
                    app_dir,
                    [APP_FILEPATH_REL_COMPOSE_RUNTIME_YML],
                    ['stop'],
                )
            )
        ])

    def _app__app__stop__rm(previous):
        return QueuedCollectionResponse(kernel, [
            InteractiveShellCommandResponse(
                kernel,
                docker_exec_app_compose_command(
                    kernel,
                    app_dir,
                    [APP_FILEPATH_REL_COMPOSE_RUNTIME_YML],
                    ['rm', '-f'],
                )
            )
        ])

    def _app__app__stop__update_hosts(previous):
        manager.log('Unregistering app')
        apps = manager.get_proxy_apps()
        if name in apps:
            del apps[name]

        manager.save_proxy_apps(apps)

        kernel.run_function(
            app__hosts__update
        )

    def _app__app__stop__complete(previous):
        manager.set_runtime_config('started', False)

        kernel.run_function(
            app__hook__exec,
            {
                'app-dir': app_dir,
                'hook': 'app/stop-post'
            }
        )

    return QueuedCollectionResponse(kernel, [
        _app__app__stop__checkup,
        _app__app__stop__stop,
        _app__app__stop__rm,
        _app__app__stop__update_hosts,
        _app__app__stop__complete,
    ])
