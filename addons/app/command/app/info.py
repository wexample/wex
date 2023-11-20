from addons.app.command.app.started import app__app__started
from addons.app.command.env.get import app__env__get
from src.const.globals import COMMAND_TYPE_ADDON
from addons.app.decorator.app_command import app_command
from src.core.response.TableResponse import TableResponse
from addons.app.AppAddonManager import AppAddonManager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Description", command_type=COMMAND_TYPE_ADDON)
def app__app__info(kernel: 'Kernel', app_dir: str):
    manager: AppAddonManager = kernel.addons['app']
    output_list = TableResponse(kernel)

    output_list.set_body([
        [
            'Name',
            manager.get_config('global.name')
        ],
        [
            'Version',
            manager.get_config('global.version')
        ],
        [
            'Status',
            'Started' if kernel.run_function(app__app__started, {
                'app-dir': app_dir,
            }).first() else 'Stopped'
        ],
        [
            'Environment',
            kernel.run_function(app__env__get, {
                'app-dir': kernel.get_path('root')
            }).first()
        ],
    ])

    return output_list
