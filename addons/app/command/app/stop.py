from addons.app.const.app import APP_FILEPATH_REL_COMPOSE_RUNTIME_YML
from addons.app.command.app.started import app__app__started, APP_STARTED_CHECK_MODE_FULL
from addons.app.helpers.docker import exec_app_docker_compose, exec_app_docker_compose_command
from addons.app.command.hook.exec import app__hook__exec
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.AppAddonManager import AppAddonManager
from src.decorator.alias_without_addon import alias_without_addon
from src.core.Kernel import Kernel
from src.decorator.command import command
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.core.response.ResponseCollectionStopResponse import ResponseCollectionStopResponse
from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from addons.app.command.app.perms import app__app__perms
from src.decorator.as_sudo import as_sudo


@command(help="Stop the given app")
@app_dir_option()
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
                    sync=False
                )
            )
        ])

    def _app__app__stop__config(previous):
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
        _app__app__stop__config,
        _app__app__stop__complete,
    ])
