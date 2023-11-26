from addons.app.command.db.exec import app__db__exec
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Set database permissions", command_type=COMMAND_TYPE_SERVICE, should_run=True)
def maria__app__first_init(manager: 'AppAddonManager', app_dir: str, service: str):
    manager.kernel.io.log('Prepare Maria users')

    manager.kernel.run_function(
        app__db__exec,
        {
            'app-dir': app_dir,
            'command': 'GRANT ALL PRIVILEGES ON *.* TO root@localhost WITH GRANT OPTION',
        }
    )

    manager.kernel.run_function(
        app__db__exec,
        {
            'app-dir': app_dir,
            'command': 'FLUSH PRIVILEGES',
        }
    )
