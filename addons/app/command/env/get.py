import os
from typing import TYPE_CHECKING, Optional

from dotenv import dotenv_values

from addons.app.const.app import APP_FILEPATH_REL_ENV
from addons.app.decorator.app_command import app_command
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager
    from src.utils.kernel import Kernel


@app_command(help="Return the property value set in the .wex/.env file")
@option(
    "--key", "-k", type=str, required=False, default="APP_ENV", help="Key in env file"
)
def app__env__get(
    manager: "AppAddonManager", app_dir: str, key: str = "APP_ENV"
) -> str:
    return _app__env__get(manager.kernel, app_dir, key)


def _app__has_env_var(app_dir: str, key: str = "APP_ENV") -> bool:
    env_file = os.path.join(app_dir, APP_FILEPATH_REL_ENV)
    # Load the environment variables from the file
    env = dotenv_values(env_file).get(key)

    return env is not None


def _app__env__get(
    kernel: "Kernel", app_dir: str, key: str = "APP_ENV", default: Optional[str] = None
) -> str:
    env_file = os.path.join(app_dir, APP_FILEPATH_REL_ENV)

    if _app__has_env_var(app_dir, key):
        env = dotenv_values(env_file).get(key)
        return str(env)
    else:
        if default is not None:
            return default
        else:
            kernel.io.error(f"Env property not found {key} in {env_file}")
            assert False
