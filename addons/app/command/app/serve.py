import click

from addons.app.command.hook.exec import app__hook__exec
from addons.app.helpers.app import app_log
from addons.app.decorator.app_dir_option import app_dir_option


@click.command()
@click.pass_obj
@app_dir_option()
def app__app__serve(kernel, app_dir: str):
    app_log(kernel, 'Serving app...')

    kernel.exec_function(
        app__hook__exec,
        {
            'app-dir': app_dir,
            'hook': 'app/serve'
        }
    )
