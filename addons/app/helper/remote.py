from typing import TYPE_CHECKING, Optional
from src.const.globals import VERBOSITY_LEVEL_MAXIMUM

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


def remote_get_environment_ip(kernel, environment: str) -> Optional[str]:
    manager: "AppAddonManager" = kernel.addons["app"]

    if manager.has_config(f"env.{environment}.server.ip"):
        ip = manager.get_config(f"env.{environment}.server.ip").get_str()
        manager.kernel.io.log(
            f"Using ip {ip}",
            verbosity=VERBOSITY_LEVEL_MAXIMUM)
        return ip
    elif manager.has_config(f"env.{environment}.domain_main"):
        domain = manager.get_config(f"env.{environment}.domain_main").get_str()
        manager.kernel.io.log(
            f"Using domain {domain}",
            verbosity=VERBOSITY_LEVEL_MAXIMUM)
        return domain

    manager.kernel.io.log(
        f"No remote domain or server IP found for env {environment}",
        verbosity=VERBOSITY_LEVEL_MAXIMUM)

    return None
