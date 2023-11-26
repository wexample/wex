from src.decorator.option import option
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Return connexion info", command_type=COMMAND_TYPE_SERVICE)
@option('--protocol', '-p', type=str, required=False, default="postgresql", help="Protocol")
def postgres__db__connect(manager: 'AppAddonManager', app_dir: str, service: str, protocol: str = 'postgresql'):
    user = manager.get_config(f'service.{service}.user')
    password = manager.get_config(f'service.{service}.password')
    name = manager.get_config(f'service.{service}.name')

    return f'{protocol}://{user}:"{password}"@localhost/{name}'
