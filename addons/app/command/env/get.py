import os

from dotenv import dotenv_values
from addons.app.const.app import APP_FILEPATH_REL_ENV
from src.decorator.option import option
from addons.app.decorator.app_command import app_command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Return the property value set in the .wex/.env file")
@option('--key', '-k', type=str, required=False, default='APP_ENV',
        help="Key in env file")
def app__env__get(kernel: 'Kernel', app_dir: str, key: str = 'APP_ENV') -> str:
    return _app__env__get(app_dir, key)


def _app__env__get(app_dir: str, key: str = 'APP_ENV') -> str:
    return dotenv_values(
        os.path.join(app_dir,
                     APP_FILEPATH_REL_ENV)).get(key)
