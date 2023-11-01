from src.core.Kernel import Kernel
from addons.app.AppAddonManager import AppAddonManager
from src.decorator.option import option
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE


@app_command(help="Return connexion info", command_type=COMMAND_TYPE_SERVICE)
@option('--protocol', '-p', type=str, required=False, default="postgresql", help="Protocol")
def postgres__db__connect(kernel: Kernel, app_dir: str, service: str, protocol: str = 'postgresql'):
    manager: AppAddonManager = kernel.addons['app']
    user = manager.get_config(f'service.{service}.user')
    password = manager.get_config(f'service.{service}.password')
    name = manager.get_config(f'service.{service}.name')

    return f'{protocol}://{user}:"{password}"@localhost/{name}'
