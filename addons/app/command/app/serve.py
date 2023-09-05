from addons.app.command.hook.exec import app__hook__exec
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.AppAddonManager import AppAddonManager
from src.decorator.command import command
from src.core.Kernel import Kernel


@command(help="Service the app if need a service to start.")
@app_dir_option()
def app__app__serve(kernel: Kernel, app_dir: str):
    manager: AppAddonManager = kernel.addons['app']
    manager.log('Serving app...')

    kernel.run_function(
        app__hook__exec,
        {
            'app-dir': app_dir,
            'hook': 'app/serve'
        }
    )
