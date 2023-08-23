import click

from addons.app.command.config.get import app__config__get

APP_STARTED_CHECK_MODE_CONFIG = 'config'


@click.command()
@click.pass_obj
@click.option('--app-dir', '-a', type=str, required=False)
@click.option('--check-mode', '-cm', type=str, required=False, default=APP_STARTED_CHECK_MODE_CONFIG)
def app__app__started(kernel, app_dir: str, check_mode: str = APP_STARTED_CHECK_MODE_CONFIG):
    config_started = kernel.exec_function(
        app__config__get,
        {
            'app-dir': app_dir,
            'default': False,
            'build': True,
            'key': 'context.started',
        }
    )

    if check_mode == APP_STARTED_CHECK_MODE_CONFIG:
        return config_started
