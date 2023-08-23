import os
from typing import Optional
import click

from addons.app.decorator.app_location_optional import app_location_optional
from addons.app.helpers.app import is_app_root


@click.command
@click.option('--app-dir', '-a', type=str, required=False,
              help="App directory")
@app_location_optional
def app__location__find(app_dir: Optional[str] = False) -> Optional[str]:
    """Search for the config file in the given directory path or its parent directories.
    Returns the path of the directory containing the config file, or None if not found.
    """

    if not app_dir:
        app_dir = os.getcwd()
    else:
        app_dir = os.path.abspath(app_dir)

    while app_dir != '/':  # Stop at root directory
        if not os.path.exists(app_dir):
            return None

        if is_app_root(app_dir):
            return f'{app_dir}/'
        app_dir = os.path.dirname(app_dir)
    return None
