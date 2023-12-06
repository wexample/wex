import os
import platform
import shutil
from typing import TYPE_CHECKING, cast

from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from src.core.command.resolver.ServiceCommandResolver import ServiceCommandResolver

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Install the proxy service", command_type=COMMAND_TYPE_SERVICE)
def proxy__service__install(
    manager: "AppAddonManager", app_dir: str, service: str
) -> None:
    def callback() -> None:
        port = 80
        port_secure = 443

        # MacOS changes (not tested inherited code)
        if platform.system() == "Darwin":
            port = 7780
            port_secure = 7743

        manager.set_config("global.port_public", port)
        manager.set_config("global.port_public_secure", port_secure)

    service_resolver = cast(
        "ServiceCommandResolver", manager.kernel.resolvers[COMMAND_TYPE_SERVICE]
    )

    shutil.copytree(
        os.path.join(
            service_resolver.get_registered_service_data("proxy")["dir"],
            "samples",
            "proxy",
        ),
        app_dir + "proxy/",
        dirs_exist_ok=True,
        copy_function=shutil.copy2,
    )

    manager.exec_in_app_workdir(app_dir, callback)
