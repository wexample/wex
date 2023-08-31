import click

from addons.app.decorator.app_dir_option import app_dir_option

APP_STARTED_CHECK_MODE_CONFIG = 'config'
APP_STARTED_CHECK_MODE_FULL = 'full'


@click.command()
@click.pass_obj
@app_dir_option()
@click.option('--check-mode', '-cm', type=str, required=False, default=APP_STARTED_CHECK_MODE_FULL,
              help="Define how to define if app is started or not")
def app__app__started(kernel, app_dir: str, check_mode: str = APP_STARTED_CHECK_MODE_FULL):
    if check_mode == APP_STARTED_CHECK_MODE_FULL or check_mode == APP_STARTED_CHECK_MODE_CONFIG:
        if not kernel.addons['app'].get_runtime_config('started', False):
            return False

    return True
