from addons.app.AppAddonManager import AppAddonManager
from src.decorator.option import option
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Enter in db console", command_type=COMMAND_TYPE_SERVICE, should_run=True)
@option('--database', '-d', type=str, required=False, help="Database name")
def sqlserver__db__go(kernel: 'Kernel', app_dir: str, service: str, database: str = None):
    manager: AppAddonManager = kernel.addons['app']
    user = manager.get_config(f'service.{service}.user')
    password = manager.get_config(f'service.{service}.password')
    name = database or manager.get_config(f'service.{service}.name')

    return f'/opt/mssql-tools/bin/sqlcmd -S localhost -U {user} -P "{password}" -d {name}'
