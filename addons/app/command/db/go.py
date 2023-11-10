from addons.app.AppAddonManager import AppAddonManager
from src.const.globals import COMMAND_CHAR_SERVICE, COMMAND_SEPARATOR_ADDON
from src.core import Kernel
from addons.app.command.app.exec import app__app__exec
from addons.app.decorator.app_command import app_command


@app_command(help="Enter into database management CLI")
def app__db__go(
        kernel: Kernel,
        app_dir: str):
    manager: AppAddonManager = kernel.addons['app']
    # There is a probable mismatch between container / service names
    # but for now each service have only one container.
    service = manager.get_config(
        'docker.main_db_container',
        required=True)

    go_command = kernel.run_command(
        f'{COMMAND_CHAR_SERVICE}{service}{COMMAND_SEPARATOR_ADDON}db/go',
        {
            'app-dir': app_dir,
            'service': service
        }
    ).first()

    kernel.run_function(
        app__app__exec,
        {
            'app-dir': app_dir,
            'container-name': service,
            'command': go_command,
            'interactive': True
        }
    )
