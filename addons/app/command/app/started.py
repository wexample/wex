import click

from addons.app.command.config.get import app__config__get

APP_STARTED_CHECK_MODE_CONFIG = 'config'
APP_STARTED_CHECK_MODE_FULL = 'full'


@click.command()
@click.pass_obj
@click.option('--app-dir', '-a', type=str, required=False)
@click.option('--check-mode', '-cm', type=str, required=False, default=APP_STARTED_CHECK_MODE_FULL)
def app__app__started(kernel, app_dir: str, check_mode: str = APP_STARTED_CHECK_MODE_FULL):
    if check_mode == APP_STARTED_CHECK_MODE_FULL or check_mode == APP_STARTED_CHECK_MODE_CONFIG:
        if not app__config__get.callback(app_dir, 'context.started', False, True):
            return False

    return True
