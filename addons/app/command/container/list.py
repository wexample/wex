
from addons.app.AppAddonManager import AppAddonManager
from addons.app.decorator.app_command import app_command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Return list of containers for given app")
def app__container__list(kernel: 'Kernel', app_dir: str):
    manager: AppAddonManager = kernel.addons['app']
    container_names = []

    if 'services' in manager.runtime_docker_compose:
        for service, attributes in manager.runtime_docker_compose['services'].items():
            container_name = attributes.get('container_name', service)
            container_names.append(container_name)

    return container_names
