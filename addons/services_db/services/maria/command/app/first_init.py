from src.core.Kernel import Kernel
from addons.app.command.db.exec import app__db__exec
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE


@app_command(help="Set database permissions", command_type=COMMAND_TYPE_SERVICE, should_run=True)
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
