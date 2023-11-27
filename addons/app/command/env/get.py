import os
from typing import TYPE_CHECKING

from dotenv import dotenv_values

from addons.app.const.app import APP_FILEPATH_REL_ENV
from addons.app.decorator.app_command import app_command
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager
    from src.core.Kernel import Kernel


@app_command(help="Return the property value set in the .wex/.env file")
@option(
    "--key", "-k", type=str, required=False, default="APP_ENV", help="Key in env file"
)
def app__env__get(
    manager: "AppAddonManager", app_dir: str, key: str = "APP_ENV"
) -> str:
    return _app__env__get(manager.kernel, app_dir, key)


def _app__env__get(kernel: "Kernel", app_dir: str, key: str = "APP_ENV") -> str:
    env = dotenv_values(os.path.join(app_dir, APP_FILEPATH_REL_ENV)).get(key)

    if not env:
        kernel.io.error(f"Env not found from APP_ENV in {app_dir}")
        assert False

    return str(env)
