from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command
from addons.app.command.db.exec import app__db__exec


@command(help="Set database permissions")
@app_dir_option()
@service_option()
def mongo__app__first_init(kernel: Kernel, app_dir: str, service: str):
    return kernel.run_function(
        app__db__exec,
        {
            'app-dir': app_dir,
            # Ask to execute bash
            'command': 'rs.initiate()',
        }
    )

