from typing import TYPE_CHECKING, Optional
from src.const.globals import VERBOSITY_LEVEL_MAXIMUM
from src.const.types import (
    StringsList,
)
from src.helper.string import string_to_snake_case

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


def remote_get_environment_ip(manager: "AppAddonManager", environment: str) -> Optional[str]:
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


def remote_get_login_command(
    manager: "AppAddonManager",
    environment: str
) -> StringsList:
    env_screaming_snake = string_to_snake_case(environment).upper()
    password = manager.get_env_var(f"ENV_{env_screaming_snake}_SERVER_PASSWORD")

    if password:
        return [
            "sshpass", "-p", password
        ]

    return []


def remote_get_connexion_command(
    manager: "AppAddonManager",
    environment: str,
    terminal: bool = False
) -> StringsList:
    command_connect = remote_get_login_command(manager, environment) + [
        "ssh",
        "-o",
        "StrictHostKeyChecking=no",
    ]

    if terminal:
        command_connect.append('-t')

    return command_connect


def remote_get_connexion_address(manager: "AppAddonManager", environment: str) -> Optional[str]:
    domain_or_ip = remote_get_environment_ip(manager, environment)

    if not domain_or_ip:
        return

    env_screaming_snake = string_to_snake_case(environment).upper()
    username = manager.get_env_var(f"ENV_{env_screaming_snake}_SERVER_USERNAME")

    if username:
        return f"{username}@{domain_or_ip}"

    return domain_or_ip
