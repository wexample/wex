from src.helper.system import set_permissions_recursively
from src.core.Kernel import Kernel
from addons.app.const.app import APP_DIR_APP_DATA
from addons.app.AppAddonManager import AppAddonManager
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE


@app_command(help="Set service permissions", command_type=COMMAND_TYPE_SERVICE)
def sqlserver__app__perms(kernel: Kernel, app_dir: str, service: str):
    manager: AppAddonManager = kernel.addons['app']
    env_dir = f'{manager.app_dir}{APP_DIR_APP_DATA}'

    # Need full permissions to start
    set_permissions_recursively(env_dir + 'sqlserver/data', 0o777)
    set_permissions_recursively(env_dir + 'sqlserver/dumps', 0o777)
    set_permissions_recursively(env_dir + 'sqlserver/log', 0o777)
    set_permissions_recursively(env_dir + 'sqlserver/mssql', 0o777)
