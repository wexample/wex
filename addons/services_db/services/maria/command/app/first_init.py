from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command
from addons.app.command.db.exec import app__db__exec


@command(help="Set database permissions")
@app_dir_option()
@service_option()
def maria__app__first_init(kernel: Kernel, app_dir: str, service: str):
    kernel.io.log('Prepare Maria users')
    
    kernel.run_function(
        app__db__exec,
        {
            'app-dir': app_dir,
            'command': 'GRANT ALL PRIVILEGES ON *.* TO root@localhost WITH GRANT OPTION',
        }
    )

    kernel.run_function(
        app__db__exec,
        {
            'app-dir': app_dir,
            'command': 'FLUSH PRIVILEGES',
        }
    )
