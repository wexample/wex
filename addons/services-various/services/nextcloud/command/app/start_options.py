import click

from addons.app.command.config.get import app__config__get


@click.command()
@click.pass_obj
@click.option('--options', '-o', required=True, default='', help="Argument")
def nextcloud__app__start_options(kernel, options: str):
    app_dir = kernel.addons['app']['config']['context']['dir']

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
