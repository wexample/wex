
from dotenv import dotenv_values
from addons.app.const.app import APP_FILEPATH_REL_ENV
from src.core.Kernel import Kernel
from src.decorator.option import option
from addons.app.decorator.app_command import app_command


@app_command(help="Return the property value set in the .wex/.env file")
@option('--key', '-k', type=str, required=False, default='APP_ENV',
        help="Key in env file")
def app__env__get(kernel: Kernel, app_dir: str, key: str = 'APP_ENV') -> str:
    config = dotenv_values(app_dir + APP_FILEPATH_REL_ENV)

    return config.get(key)
