from addons.app.AppAddonManager import AppAddonManager
from src.const.globals import COMMAND_CHAR_SERVICE, COMMAND_SEPARATOR_ADDON
from src.decorator.command import command
from src.core import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.command.app.exec import app__app__exec
from src.decorator.alias_without_addon import alias_without_addon
from src.decorator.option import option


@command(help="Execute command in database container service")
@alias_without_addon()
@app_dir_option()
@option('--command', '-c', type=str, required=True, help="Command to execute in database")
@option('--database', '-d', type=str, required=False, help="Database name")
@option('--service', '-s', type=str, required=False, help="Database service name")
def app__db__exec(
        kernel: Kernel,
        app_dir: str,
        command: str,
        service: str = None,
        database: str = None):
    manager: AppAddonManager = kernel.addons['app']
    service = service or manager.get_config('docker.main_db_container')

    exec_command = kernel.run_command(
        f'{COMMAND_CHAR_SERVICE}{service}{COMMAND_SEPARATOR_ADDON}db/exec',
        {
            'app-dir': app_dir,
            'service': service,
            'command': command,
            'database': database
        }
    ).first()

    return kernel.run_function(
        app__app__exec,
        {
            'app-dir': app_dir,
            'container-name': service,
            'command': exec_command
        }
    )
