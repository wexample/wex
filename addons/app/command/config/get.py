import click
from addons.app.const.app import APP_FILEPATH_REL_CONFIG, APP_FILEPATH_REL_CONFIG_BUILD
from src.helper.file import get_yml_file_item


@click.command
@click.option('--key', '-k', type=str, required=True,
              help="Key in config file")
@click.option('--default', '-d', required=False,
              help="Default returned value if not found in config file")
@click.option('--build', '-b', is_flag=True, required=False, default=False,
              help="Edit auto generated config or source config (default)")
@click.option('--app-dir', '-a', type=str, required=True,
              help="App directory")
def app__config__get(key: str, default: str = None, build: bool = False, app_dir: str = None):
    if build:
        config_file = APP_FILEPATH_REL_CONFIG_BUILD
    else:
        config_file = APP_FILEPATH_REL_CONFIG

    return get_yml_file_item(
        config_file,
        key,
        default
    )
