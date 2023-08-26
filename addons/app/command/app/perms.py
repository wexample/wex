import click

from addons.app.command.hook.exec import app__hook__exec
from addons.app.helpers.app import app_log


@click.command()
@click.pass_obj
@click.option('--app-dir', '-a', type=str, required=True,
              help="App directory")
def app__app__perms(kernel, app_dir: str):
    app_log(kernel, 'Updating app permissions...')
    kernel.exec_function(
        app__hook__exec,
        {
            'app-dir': app_dir,
            'hook': 'app/perms'
        }
    )
