import getpass
import os.path
from typing import TYPE_CHECKING, Optional, cast

from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.app.init import app__app__init
from addons.app.command.app.start import app__app__start
from addons.app.command.app.started import app__app__started
from addons.app.command.env.get import app__env__get
from src.core.response.AbstractResponse import AbstractResponse
from src.core.response.queue_collection.AbstractQueuedCollectionResponseQueueManager import (
    AbstractQueuedCollectionResponseQueueManager,
)
from src.core.response.queue_collection.QueuedCollectionStopResponse import (
    QueuedCollectionStopResponse,
)
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from src.decorator.option import option
from src.helper.process import process_get_all_by_port

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@as_sudo()
@command(help="Create and start the reverse proxy server")
@option("--user", "-u", type=str, required=False, help="Owner of application files")
@option("--env", "-e", type=str, required=False, help="Env for accessing apps")
@option("--group", "-g", type=str, required=False, help="Group of application files")
@option("--port", "-p", type=int, required=False, help="Port for web server")
@option(
    "--port-secure", "-ps", type=int, required=False, help="Secure port for web server"
)
def app__proxy__start(
    kernel: "Kernel",
    env: Optional[str] = None,
    user: Optional[str] = None,
    group: Optional[str] = None,
    port: Optional[str] = None,
    port_secure: Optional[str] = None,
) -> QueuedCollectionResponse:
    manager: AppAddonManager = cast(AppAddonManager, kernel.addons["app"])
    proxy_path = manager.get_proxy_path()

    def _app__proxy__start__create(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> Optional[QueuedCollectionStopResponse]:
        manager.log("Starting proxy server")

        # Created
        if manager.is_app_root(proxy_path):
            # Started
            if kernel.run_function(
                app__app__started,
                {
                    "app-dir": proxy_path,
                },
            ).first():
                return QueuedCollectionStopResponse(kernel, "PROXY_STARTED")
        else:
            manager.log(f"Creating proxy dir {proxy_path}")
            os.makedirs(proxy_path, exist_ok=True)

            kernel.run_function(
                app__app__init,
                {"app-dir": proxy_path, "services": ["proxy"], "git": False},
            )

    def _app__proxy__start__checkup(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> None:
        def _callback() -> None:
            nonlocal user
            user = user or getpass.getuser()

            def check_port(port_to_check: int) -> None:
                if not port_to_check:
                    kernel.io.error(f"Invalid port {port_to_check}", trace=False)

                manager.log(f"Checking that port {port_to_check} is free")

                # Check port availability.
                process = process_get_all_by_port(port_to_check)
                if process:
                    kernel.io.error(
                        f"Process {process.pid} ({process.name()}) is using port {port_to_check}",
                        trace=False,
                    )

                kernel.io.success(f"Port {port_to_check} free")

            check_port(manager.get_config("global.port_public"))
            check_port(manager.get_config("global.port_public_secure"))

        manager.exec_in_app_workdir(proxy_path, _callback)

    def _app__proxy__start__start(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> AbstractResponse:
        return kernel.run_function(
            app__app__start,
            {
                "app-dir": proxy_path,
                # If no env, use the global wex env.
                "env": env
                       or kernel.run_function(
                    app__env__get, {"app-dir": kernel.get_path("root")}
                ).first(),
                "user": user,
                "group": group,
            },
        )

    return QueuedCollectionResponse(
        kernel,
        [
            _app__proxy__start__create,
            _app__proxy__start__checkup,
            _app__proxy__start__start,
        ],
    )
