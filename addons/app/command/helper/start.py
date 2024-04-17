import getpass
import os.path
from typing import TYPE_CHECKING, Optional, cast, Any

from click import Choice

from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.app.init import app__app__init
from addons.app.command.app.start import app__app__start
from addons.app.command.app.started import app__app__started
from addons.app.const.app import HELPER_APPS_LIST
from src.helper.prompt import prompt_progress_steps
from src.core.response.AbstractResponse import AbstractResponse
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from src.decorator.option import option
from src.helper.system import system_port_check

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@as_sudo()
@command(help=f"Create and start a helper app {','.join(HELPER_APPS_LIST)}")
@option(
    "--name",
    "-n",
    type=Choice(HELPER_APPS_LIST),
    required=True,
    help=f"One of helper app name : {','.join(HELPER_APPS_LIST)}",
)
@option("--user", "-u", type=str, required=False, help="Owner of application files")
@option(
    "--create-network",
    "-cn",
    type=bool,
    required=True,
    default=True,
    help="Creates a docker network",
)
@option("--env", "-e", type=str, required=False, help="Env for accessing apps")
@option("--group", "-g", type=str, required=False, help="Group of application files")
@option("--port", "-p", type=int, required=False, help="Port for web server")
@option(
    "--port-secure", "-ps", type=int, required=False, help="Secure port for web server"
)
def app__helper__start(
    kernel: "Kernel",
    name: str,
    create_network: bool,
    env: Optional[str] = None,
    user: Optional[str] = None,
    group: Optional[str] = None,
    port: Optional[int] = None,
    port_secure: Optional[int] = None,
) -> str:
    manager: AppAddonManager = cast(AppAddonManager, kernel.addons["app"])
    # App name is same of main service
    helper_service_name = name
    helper_app_path = manager.get_helper_app_path(name, env)

    def _app__helper__start__create() -> Any:
        nonlocal env
        kernel.io.log("Starting helper app")

        # Created
        if manager.is_app_root(helper_app_path):
            # Started
            if kernel.run_function(
                app__app__started,
                {
                    "app-dir": helper_app_path,
                },
            ).first():
                return False

        kernel.io.log(f"Creating helper app dir : {helper_app_path}")
        os.makedirs(helper_app_path, exist_ok=True)

        return kernel.run_function(
            app__app__init,
            {
                "app-dir": helper_app_path,
                "services": [helper_service_name],
                "git": False,
                "env": env,
            },
        )

    def _app__helper__start__checkup() -> None:
        def _callback() -> None:
            nonlocal user
            nonlocal port
            nonlocal port_secure

            user = user or getpass.getuser()

            # Override default service ports
            if port:
                system_port_check(kernel, port)
                manager.set_config(f"service.{helper_service_name}.port_public", port)

            if port_secure:
                system_port_check(kernel, port_secure)
                manager.set_config(
                    f"service.{helper_service_name}.port_public_secure", port_secure
                )

        manager.exec_in_app_workdir(helper_app_path, _callback)

        if not create_network:
            manager.set_config("docker.create_network", create_network)

    def _app__helper__start__start() -> AbstractResponse:
        nonlocal env

        return kernel.run_function(
            app__app__start,
            {
                "app-dir": helper_app_path,
                # If no env, use the global wex env.
                "env": env,
                "user": user,
                "group": group,
            },
        )

    prompt_progress_steps(
        kernel,
        [
            _app__helper__start__create,
            _app__helper__start__checkup,
            _app__helper__start__start,
        ],
    )

    return helper_app_path
