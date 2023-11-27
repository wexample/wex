from typing import TYPE_CHECKING

from addons.app.command.app.exec import app__app__exec
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_CHAR_SERVICE, COMMAND_SEPARATOR_ADDON

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Enter into database management CLI")
def app__db__go(
        manager: 'AppAddonManager',
        app_dir: str):
    # There is a probable mismatch between container / service names
    # but for now each service have only one container.
    service = manager.get_config(
        'docker.main_db_container',
        required=True)

    go_command = manager.kernel.run_command(
        f'{COMMAND_CHAR_SERVICE}{service}{COMMAND_SEPARATOR_ADDON}db/go',
        {
            'app-dir': app_dir,
            'service': service
        }
    ).first()

    manager.kernel.run_function(
        app__app__exec,
        {
            'app-dir': app_dir,
            'container-name': service,
            'command': go_command,
            'interactive': True
        }
    )
