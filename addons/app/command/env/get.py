import click

from dotenv import dotenv_values
from addons.app.const.app import APP_FILEPATH_REL_ENV


@click.command
@click.option('--key', '-k', type=str, required=False, default='APP_ENV')
@click.option('--app-dir', '-a', type=str, required=False)
def app__env__get(key: str = 'APP_ENV', app_dir: str = './') -> str:
    config = dotenv_values(app_dir + APP_FILEPATH_REL_ENV)

    return config.get(key)
