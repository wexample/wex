import click

from addons.app.command.config.get import app__config__get
from addons.app.decorator.app_dir_option import app_dir_option


@click.command()
@click.pass_obj
@app_dir_option()
@click.option('--options', '-o', required=True, default='', help="Argument")
def nextcloud__app__start_options(kernel, app_dir, options: str):
    # On first start, do not run nextcloud until database is initialized.
    if not app__config__get.callback(
            app_dir,
            'global.initialized',
            False
    ):
        return [
            '--scale',
            f'{app__config__get.callback(app_dir, "global.name")}_nextcloud=0'
        ]
