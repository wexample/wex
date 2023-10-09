from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command
from addons.app.command.config.bind_files import app__config__bind_files


@command(help="Set configuration")
@app_dir_option()
@service_option()
def php_8__config__runtime(kernel: Kernel, app_dir: str, service: str):
    kernel.run_function(
        app__config__bind_files,
        {
            'app-dir': app_dir,
            'dir': 'php'
        }
    )

    #   TODO : legacy, should be removed.
    kernel.run_function(
        app__config__bind_files,
        {
            'app-dir': app_dir,
            'dir': 'apache'
        }
    )

