from typing import TYPE_CHECKING, Callable, List

from addons.app.command.app.perms import app__app__perms
from addons.app.command.app.started import app__app__started
from addons.app.command.hook.exec import app__hook__exec
from addons.app.command.hosts.update import app__hosts__update
from addons.app.const.app import APP_FILEPATH_REL_COMPOSE_RUNTIME_YML
from addons.app.decorator.app_command import app_command
from addons.app.helper.docker import docker_exec_app_compose_command
from src.decorator.as_sudo import as_sudo
from src.decorator.option import option
from src.helper.command import execute_command_sync
from src.helper.prompt import prompt_progress_steps

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@as_sudo()
@app_command(help="Stop the given app")
@option("--fast", "-f", is_flag=True, required=False, help="Do not rewrite config")
def app__app__stop(
    manager: "AppAddonManager",
    app_dir: str,
    fast: bool = False,
) -> None:
    kernel = manager.kernel
    name = manager.get_app_name()

    def _app__app__stop__checkup() -> bool:
        if not kernel.run_function(app__app__started, {"app-dir": app_dir}).first():
            manager.log("App already stopped")
            return False

        kernel.run_function(app__app__perms, {"app-dir": app_dir})

        return True

    def _app__app__stop__stop() -> None:
        kernel.run_function(
            app__hook__exec, {"app-dir": app_dir, "hook": "app/stop-pre"}
        )

        execute_command_sync(
            kernel,
            command=docker_exec_app_compose_command(
                kernel,
                app_dir,
                [APP_FILEPATH_REL_COMPOSE_RUNTIME_YML],
                ["stop"],
            ),
            working_directory=app_dir,
            interactive=True,
        )

    def _app__app__stop__rm() -> None:
        execute_command_sync(
            kernel,
            command=docker_exec_app_compose_command(
                kernel,
                app_dir,
                [APP_FILEPATH_REL_COMPOSE_RUNTIME_YML],
                ["rm", "-f"],
            ),
            working_directory=app_dir,
            interactive=True,
        )

    def _app__app__stop__update_hosts() -> None:
        if manager.require_proxy():
            manager.log("Unregistering app")
            apps = manager.get_proxy_apps()
            if name in apps:
                del apps[name]

            manager.save_proxy_apps(apps, manager.get_env())

        kernel.run_function(app__hosts__update)

    def _app__app__stop__complete() -> None:
        manager.set_runtime_config("started", False)

        kernel.run_function(
            app__hook__exec, {"app-dir": app_dir, "hook": "app/stop-post"}
        )

    steps: List[Callable]
    if fast:
        steps = [
            # Just load docker compose
            _app__app__stop__rm,
        ]
    else:
        steps = [
            _app__app__stop__checkup,
            _app__app__stop__stop,
            _app__app__stop__rm,
            _app__app__stop__update_hosts,
            _app__app__stop__complete,
        ]

    prompt_progress_steps(
        kernel,
        steps,
    )
