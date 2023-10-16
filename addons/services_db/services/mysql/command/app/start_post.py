import time

from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command
from addons.app.command.app.exec import app__app__exec


@command(help="Set database permissions")
@app_dir_option()
@service_option()
def mysql__app__start_post(kernel: Kernel, app_dir: str, service: str):
    # Wait loop
    while not mysql_is_ready(kernel, app_dir, service):
        kernel.io.log('Waiting for MySQL to be ready...')

        time.sleep(5)

    kernel.io.success('MySQL is ready...')


def mysql_is_ready(kernel, app_dir, service):
    response = kernel.run_function(
        app__app__exec, {
            'app-dir': app_dir,
            'container-name': service,
            'command': ['mysqladmin', 'ping']
        }
    )

    return response.success
