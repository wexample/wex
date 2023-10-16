import os.path

from addons.app.helpers.db import get_db_service_dumps_path
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command
from src.decorator.option import option
from addons.app.command.app.exec import app__app__exec
from addons.services_db.services.sqlserver.command.db.exec import sqlserver__db__exec
from src.const.globals import COMMAND_TYPE_SERVICE


@command(help="Set database permissions")
@app_dir_option()
@service_option()
@option('--file-name', '-f', type=str, required=True, help="Dump file name")
def sqlserver__db__dump(kernel: Kernel, app_dir: str, service: str, file_name: str):
    file_name += '.bak'

    exec_command = kernel.run_function(
        sqlserver__db__exec,
        {
            'app-dir': app_dir,
            'service': service,
            'command': f"BACKUP DATABASE [master] TO DISK = '/var/opt/mssql/dumps/{file_name}'"
        },
        type=COMMAND_TYPE_SERVICE
    ).first()

    kernel.run_function(
        app__app__exec,
        {
            'app-dir': app_dir,
            'container-name': service,
            # Ask to execute bash
            'command': exec_command,
            'sync': True
        }
    )

    kernel.run_function(
        app__app__exec,
        {
            'app-dir': app_dir,
            'container-name': service,
            'user': 'root',
            # Ask to execute bash
            'command': [
                'chown',
                '1000:1000',
                f'/var/opt/mssql/dumps/{file_name}'
            ],
            'sync': True
        }
    )

    return os.path.join(
        get_db_service_dumps_path(kernel, service),
        file_name)
