from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from src.helper.args import args_parse_one
from src.const.types import BasicInlineValue
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Set a configuration setting for given app")
@option("--key", "-k", type=str, required=True, help="Key in config file")
@option("--value", "-v", required=True, help="Value to set")
def app__config__set(
    manager: "AppAddonManager", app_dir: str, key: str, value: BasicInlineValue
) -> None:
    manager.set_config(
        key,
        args_parse_one(value))
