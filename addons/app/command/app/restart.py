import click

from addons.app.command.app.start import app__app__start
from addons.app.command.app.stop import app__app__stop
from addons.app.decorator.app_dir_option import app_dir_option

from src.core.Kernel import Kernel
from src.decorator.command import command


@command(help="Restarts app")
@app_dir_option()
def app__app__restart(kernel: Kernel, app_dir: str):
    kernel.run_function(
        app__app__stop,
        {
            'app-dir': app_dir
        }
    )

    kernel.run_function(
        app__app__start,
        {
            'app-dir': app_dir
        }
    )
