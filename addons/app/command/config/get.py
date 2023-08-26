import click
from addons.app.helpers.app import app_exec_in_workdir
from src.helper.file import get_dict_item_by_path


@click.command
@click.pass_obj
@click.option('--key', '-k', type=str, required=True,
              help="Key in config file")
@click.option('--default', '-d', required=False,
              help="Default returned value if not found in config file")
@click.option('--build', '-b', is_flag=True, required=False, default=False,
              help="Edit auto generated config or source config (default)")
@click.option('--app-dir', '-a', type=str, required=True,
              help="App directory")
def app__config__get(kernel, app_dir: str, key: str, default: str = None, build: bool = False):
    return app_exec_in_workdir(
        kernel,
        app_dir,
        # Callback
        lambda: get_dict_item_by_path(
            kernel.addons['app']['config' if not build else 'config_build'],
            key,
            default
        )
    )
