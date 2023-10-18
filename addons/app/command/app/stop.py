from addons.app.const.app import APP_FILEPATH_REL_COMPOSE_RUNTIME_YML
from addons.app.command.app.started import app__app__started, APP_STARTED_CHECK_MODE_FULL
from addons.app.helpers.docker import exec_app_docker_compose_command
from addons.app.command.hook.exec import app__hook__exec
from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.hosts.update import app__hosts__update
from src.decorator.alias_without_addon import alias_without_addon
from src.core.Kernel import Kernel
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.core.response.ResponseCollectionStopResponse import ResponseCollectionStopResponse
from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from addons.app.command.app.perms import app__app__perms
from src.decorator.as_sudo import as_sudo
from addons.app.decorator.app_command import app_command


@app_command(help="Stop the given app")
@alias_without_addon()
@as_sudo
def app__app__stop(kernel: Kernel, app_dir: str):
    manager: AppAddonManager = kernel.addons['app']
    name = manager.get_config('global.name')

    def _app__app__stop__checkup():
        if not kernel.run_function(app__app__started, {
            'app-dir': app_dir,
            'mode': APP_STARTED_CHECK_MODE_FULL
        }).first():
            manager.log('App already stopped')
            return ResponseCollectionStopResponse(kernel)

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

        return ResponseCollectionResponse(kernel, [
            InteractiveShellCommandResponse(
                kernel,
                exec_app_docker_compose_command(
                    kernel,
                    app_dir,
                    [APP_FILEPATH_REL_COMPOSE_RUNTIME_YML],
                    ['down'],
                )
            )
        ])

    def _app__app__stop__update_hosts(previous):
        manager.log('Unregistering app')
        if name in manager.proxy_apps:
            del manager.proxy_apps[name]

        manager.save_proxy_apps()

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

    return ResponseCollectionResponse(kernel, [
        _app__app__stop__checkup,
        _app__app__stop__stop,
        _app__app__stop__update_hosts,
        _app__app__stop__complete,
    ])
