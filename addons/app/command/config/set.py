import click
from addons.app.const.app import APP_FILEPATH_REL_CONFIG, APP_FILEPATH_REL_CONFIG_BUILD
from src.helper.file import set_yml_file_item
from addons.app.decorator.app_dir_option import app_dir_option


@click.command
@click.option('--key', '-k', type=str, required=True,
              help="Key in config file")
@click.option('--value', '-v', required=True,
              help="Value to set")
@click.option('--build', '-b', is_flag=True, required=False, default=False,
              help="Edit auto generated config or source config (default)")
@app_dir_option()
def app__config__set(app_dir: str, key: str, value, build: bool = False):
    if build:
        config_file = APP_FILEPATH_REL_CONFIG_BUILD
    else:
        config_file = APP_FILEPATH_REL_CONFIG

    set_yml_file_item(
        f'{app_dir}{config_file}',
        key,
        value
    )
