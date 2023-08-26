import click

from addons.app.command.app.start import app__app__start
from addons.app.command.app.stop import app__app__stop


@click.command(help="Restarts app")
@click.pass_obj
@click.option('--app-dir', '-a', type=str, required=True,
              help="App directory")
def app__app__restart(kernel, app_dir: str):
    kernel.exec_function(
        app__app__stop,
        {
            'app-dir': app_dir
        }
    )

    kernel.exec_function(
        app__app__start,
        {
            'app-dir': app_dir
        }
    )
