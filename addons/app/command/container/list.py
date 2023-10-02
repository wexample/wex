
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.AppAddonManager import AppAddonManager
from src.decorator.command import command
from src.core import Kernel


@command(help="Return list of containers for given app")
@app_dir_option()
def app__container__list(kernel: Kernel, app_dir: str):
    manager: AppAddonManager = kernel.addons['app']
    container_names = []

    if 'services' in manager.runtime_docker_compose:
        for service, attributes in manager.runtime_docker_compose['services'].items():
            container_name = attributes.get('container_name', service)
            container_names.append(container_name)

    return container_names
