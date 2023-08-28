import click

from dotenv import dotenv_values
from addons.app.const.app import APP_FILEPATH_REL_ENV
from addons.app.decorator.app_dir_option import app_dir_option


@click.command
@click.option('--key', '-k', type=str, required=False, default='APP_ENV',
              help="Key in env file")
@app_dir_option()
def app__env__get(app_dir: str, key: str = 'APP_ENV') -> str:
    config = dotenv_values(app_dir + APP_FILEPATH_REL_ENV)

    return config.get(key)
