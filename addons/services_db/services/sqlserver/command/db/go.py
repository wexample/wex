from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command
from addons.app.AppAddonManager import AppAddonManager
from src.decorator.option import option


@command(help="Go to database")
@app_dir_option()
@service_option()
@option('--database', '-d', type=str, required=False, help="Database name")
def sqlserver__db__go(kernel: Kernel, app_dir: str, service: str, database: str = None):
    manager: AppAddonManager = kernel.addons['app']
    user = manager.get_config(f'service.{service}.user')
    password = manager.get_config(f'service.{service}.password')
    name = database or manager.get_config(f'service.{service}.name')

    return f'/opt/mssql-tools/bin/sqlcmd -S localhost -U {user} -P "{password}" -d {name}'
