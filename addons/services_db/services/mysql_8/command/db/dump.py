import os.path

from addons.services_db.services.mysql_8.command.db.connect import mysql_8__db__connect
from addons.app.const.app import APP_DIR_APP_DATA
from src.const.globals import COMMAND_TYPE_SERVICE
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command
from addons.app.AppAddonManager import AppAddonManager
from src.decorator.option import option
from addons.app.command.app.exec import app__app__exec


@command(help="Set database permissions")
@app_dir_option()
@service_option()
@option('--file-name', '-f', type=str, required=False, help="Dump file name")
def mysql_8__db__dump(kernel: Kernel, app_dir: str, service: str, file_name):
    manager: AppAddonManager = kernel.addons['app']

    file_name += '.sql'

    command = [
        'mysqldump',
        kernel.run_function(
            mysql_8__db__connect,
            {
                'app-dir': app_dir,
                'service': service,
            },
            type=COMMAND_TYPE_SERVICE
        ).first(),
        manager.get_config('global.name'),
        '>',
        '/var/www/dumps/' + file_name
    ]

    env_dir = f'{manager.app_dir}{APP_DIR_APP_DATA}'

    kernel.run_function(
        app__app__exec,
        {
            'app-dir': app_dir,
            'container-name': service,
            # Ask to execute bash
            'command': command,
            'sync': True
        }
    )

    return os.path.join(env_dir, 'mysql', 'dumps', file_name)
