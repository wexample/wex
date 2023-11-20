from addons.app.command.config.bind_files import app__config__bind_files
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Set runtime configuration", command_type=COMMAND_TYPE_SERVICE)
def php__config__runtime(kernel: 'Kernel', app_dir: str, service: str):
    kernel.run_function(
        app__config__bind_files,
        {
            'app-dir': app_dir,
            'dir': 'php'
        }
    )


