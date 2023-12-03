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
    # Save config
    domain_pma = manager.get_runtime_config("domain_pma", None)
    assert isinstance(domain_pma, str | bool | None)

    # Setting false to domain will disable domain setting,
    # used to disable phpmyadmin in some environment.
    if isinstance(domain_pma, str) and domain_pma:
        if domain_pma is None:
            env = str(manager.get_runtime_config("env"))

            domain_pma_list: StringsList = ["pma"]
            if env != APP_ENV_LOCAL and env != APP_ENV_PROD:
                domain_pma_list.append(env)

            domain_pma_list.append(str(manager.get_runtime_config("domain_tld")))

            domain_pma = ".".join(domain_pma_list)

            manager.set_runtime_config("domain_pma", domain_pma)

        domains = cast(StringsList, manager.get_runtime_config("domains", []))
        assert isinstance(domains, list)

        domains.append(domain_pma)

        manager.set_runtime_config("domains", domains)
