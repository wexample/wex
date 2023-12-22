from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from src.decorator.option import option
from src.helper.args import args_parse_one

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Set a configuration setting for given app")
@option("--key", "-k", type=str, required=True, help="Key in config file")
@option("--value", "-v", type=str, required=True, help="Value to set")
def app__config__set(
    manager: "AppAddonManager", app_dir: str, key: str, value: str
) -> None:
    manager.set_config(key, args_parse_one(value))
