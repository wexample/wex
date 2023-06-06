import click
from addons.app.const.app import APP_FILEPATH_REL_CONFIG, APP_FILEPATH_REL_CONFIG_BUILD
from src.helper.file import set_json_file_item


@click.command
@click.option('--key', '-k', type=str, required=True)
@click.option('--value', '-v', required=True)
@click.option('--build', '-b', is_flag=True, required=False, default=False)
@click.option('--app-dir', '-a', type=str, required=False)
def app__config__set(key, value, build: bool = False, app_dir: str = None):
    if build:
        config_file = APP_FILEPATH_REL_CONFIG_BUILD
    else:
        config_file = APP_FILEPATH_REL_CONFIG

    set_json_file_item(
        config_file,
        key,
        value
    )
