
from addons.app.AppAddonManager import AppAddonManager
from src.core import Kernel
from addons.app.decorator.app_command import app_command


@app_command(help="Return list of containers for given app")
def app__container__list(kernel: Kernel, app_dir: str):
    manager: AppAddonManager = kernel.addons['app']
    container_names = []

    if 'services' in manager.runtime_docker_compose:
        for service, attributes in manager.runtime_docker_compose['services'].items():
            container_name = attributes.get('container_name', service)
            container_names.append(container_name)

    return container_names
