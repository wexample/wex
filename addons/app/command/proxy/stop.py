import click

from addons.app.command.app.stop import app__app__stop
from addons.app.decorator.app_location_optional import app_location_optional
from src.decorator.as_sudo import as_sudo
from addons.app.helpers.app import app_exec_in_workdir


@click.command()
@click.pass_obj
@as_sudo
@app_location_optional
def app__proxy__stop(kernel):
    proxy_path = kernel.addons['app']['path']['proxy']

    def callback():
        kernel.exec_function(
            app__app__stop,
            {
                'app-dir': proxy_path
            }
        )

    return app_exec_in_workdir(
        kernel,
        proxy_path,
        callback
    )
