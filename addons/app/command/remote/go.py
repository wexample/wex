from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from src.decorator.option import option
from src.core import Kernel
from src.const.globals import COMMAND_TYPE_ADDON
from addons.app.AppAddonManager import AppAddonManager
from addons.app.decorator.app_command import app_command


@app_command(help="Description", command_type=COMMAND_TYPE_ADDON)
@option('--environment', '-e', type=str, required=True, help="Remote environment (dev, prod)")
def app__remote__go(kernel: Kernel, app_dir: str, environment: str):
    manager: AppAddonManager = kernel.addons['app']

    domain = manager.get_config(f'env.{environment}.domain_main')

    if not domain:
        return

    return InteractiveShellCommandResponse(kernel, [
        'ssh',
        domain
    ])
