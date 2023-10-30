from addons.app.command.app.started import app__app__started
from addons.app.command.env.get import app__env__get
from src.core import Kernel
from src.const.globals import COMMAND_TYPE_ADDON
from addons.app.decorator.app_command import app_command
from src.core.response.DataSet2dResponse import DataSet2dResponse
from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Description", command_type=COMMAND_TYPE_ADDON)
def app__app__info(kernel: Kernel, app_dir: str):
    manager: AppAddonManager = kernel.addons['app']
    output_list = DataSet2dResponse(kernel)

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
