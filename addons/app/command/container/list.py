from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from src.const.types import StringsList

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Return list of containers for given app")
def app__container__list(manager: "AppAddonManager", app_dir: str) -> StringsList:
    container_names = []

    if manager.runtime_docker_compose and "services" in manager.runtime_docker_compose:
        for service, attributes in manager.runtime_docker_compose["services"].items():
            container_name = attributes.get("container_name", service)
            container_names.append(container_name)

    return container_names
