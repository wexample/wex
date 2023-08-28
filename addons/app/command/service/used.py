import click

from addons.app.command.config.get import app__config__get
from addons.app.decorator.app_dir_option import app_dir_option


@click.command()
@click.pass_obj
@app_dir_option()
@click.option('--service', '-s', type=str, required=True,
              help="Service name to check in app configuration")
def app__service__used(kernel, service, app_dir):
    return service in kernel.exec_function(
        app__config__get,
        {
            'key': 'global.services',
            'app-dir': app_dir
        }
    )
