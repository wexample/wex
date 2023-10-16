import os.path

from addons.services_db.services.postgres.command.db.connect import postgres__db__connect
from addons.app.helpers.db import get_db_service_dumps_path
from src.const.globals import COMMAND_TYPE_SERVICE
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command
from src.decorator.option import option
from addons.app.command.app.exec import app__app__exec


@command(help="Set database permissions")
@app_dir_option()
@service_option()
@option('--file-name', '-f', type=str, required=True, help="Dump file name")
def postgres__db__dump(kernel: Kernel, app_dir: str, service: str, file_name: str):
    file_name += '.sql'

    command = [
        'pg_dump',
        kernel.run_function(
            postgres__db__connect,
            {
                'app-dir': app_dir,
                'service': service,
            },
            type=COMMAND_TYPE_SERVICE
        ).first(),
        '-f',
        '/var/www/dumps/' + file_name
    ]

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

    return os.path.join(
        get_db_service_dumps_path(kernel, service),
        file_name)


