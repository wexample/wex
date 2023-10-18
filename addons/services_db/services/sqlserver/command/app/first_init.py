from src.core.Kernel import Kernel
from addons.app.command.db.exec import app__db__exec
from addons.app.AppAddonManager import AppAddonManager
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE


@app_command(help="Init database", command_type=COMMAND_TYPE_SERVICE, should_run=True)
def sqlserver__app__first_init(kernel: Kernel, app_dir: str, service: str):
    manager: AppAddonManager = kernel.addons['app']

    re = kernel.run_function(
        app__db__exec,
        {
            'app-dir': app_dir,
            'database': 'master',
            # Ask to execute bash
            'command': f'CREATE DATABASE {manager.get_config("global.name")}',
        }
    )

    return re