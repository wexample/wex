from addons.app.command.hook.exec import app__hook__exec
from addons.app.AppAddonManager import AppAddonManager
from addons.app.decorator.app_command import app_command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Service the app if need a service to start.")
def app__app__serve(kernel: 'Kernel', app_dir: str):
    manager: AppAddonManager = kernel.addons['app']
    manager.log('Serving app...')

    kernel.run_function(
        app__hook__exec,
        {
            'app-dir': app_dir,
            'hook': 'app/serve'
        }
    )
