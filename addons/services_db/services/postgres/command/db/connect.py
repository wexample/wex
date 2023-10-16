from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command
from addons.app.AppAddonManager import AppAddonManager


@command(help="Return connexion info")
@app_dir_option()
@service_option()
def postgres__db__connect(kernel: Kernel, app_dir: str, service: str):
    manager: AppAddonManager = kernel.addons['app']
    user = manager.get_config(f'service.{service}.user')
    password = manager.get_config(f'service.{service}.password')
    name = manager.get_config(f'service.{service}.name')

    return f'postgresql://{user}:"{password}"@localhost/{name}'
