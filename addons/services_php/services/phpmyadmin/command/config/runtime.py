from typing import TYPE_CHECKING, cast

from addons.app.const.app import APP_ENV_LOCAL, APP_ENV_PROD
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from src.const.types import StringsList

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Set runtime configuration", command_type=COMMAND_TYPE_SERVICE)
def phpmyadmin__config__runtime(
    manager: "AppAddonManager", app_dir: str, service: str
) -> None:
    if not manager.has_runtime_config("domain_pma"):
        env = manager.get_runtime_config("env").get_str()

        domain_pma_list: StringsList = ["pma"]
        if env != APP_ENV_LOCAL and env != APP_ENV_PROD:
            domain_pma_list.append(env)

        domain_pma_list.append(manager.get_runtime_config("domain_tld").get_str())

        domain_pma = ".".join(domain_pma_list)

        manager.set_runtime_config("domain_pma", domain_pma)
        return

    # Setting false to domain will disable domain setting,
    # used to disable phpmyadmin in some environment.
    domain_pma_value = manager.get_runtime_config("domain_pma")
    if domain_pma_value.is_bool() and domain_pma_value.get_bool() is False:
        return

    domain_pma = domain_pma_value.get_str()
    domains = cast(StringsList, manager.get_runtime_config("domains", []).get_list())
    domains.append(domain_pma)
    manager.set_runtime_config("domains", domains)
