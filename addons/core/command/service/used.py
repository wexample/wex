import click

from addons.app.command.config.get import app__config__get


@click.command()
@click.pass_obj
@click.option('--app-dir', '-a', type=str, required=False)
@click.option('--service', '-s', type=str, required=True)
def app_service_used(kernel, service, app_dir):
    return service in kernel.exec_function(
        app__config__get,
        {
            'key': 'global.services',
            'app-dir': app_dir
        }
    )
