import os
import shutil
from typing import TYPE_CHECKING, cast

from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Install the proxy service", command_type=COMMAND_TYPE_SERVICE)
def proxy__service__install(
        manager: "AppAddonManager", app_dir: str, service: str
) -> None:
    from wexample_wex_core.resolver.service_command_resolver import ServiceCommandResolver

    def callback() -> None:
        manager.set_config(
            "port.public", manager.get_config("port.public", default=80).get_int()
        )

        manager.set_config(
            "port.public_secure",
            manager.get_config("port.public_secure", default=443).get_int(),
        )

    service_resolver = cast(
        ServiceCommandResolver,
        manager.kernel.resolvers[COMMAND_TYPE_SERVICE]
    )

    shutil.copytree(
        os.path.join(
            service_resolver.get_registered_service_data(service)["dir"],
            "samples",
            "proxy",
        ),
        app_dir + "proxy/",
        dirs_exist_ok=True,
        copy_function=shutil.copy2,
    )

    manager.exec_in_app_workdir(app_dir, callback)
