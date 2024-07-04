from typing import TYPE_CHECKING

from addons.app.const.app import APP_DIR_APP_DATA_NAME
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from wexample_helpers.helpers.dict_helper import DICT_ITEM_EXISTS_ACTION_MERGE
from src.helper.string import string_random_password

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Install database service", command_type=COMMAND_TYPE_SERVICE)
def mysql__service__install(
    manager: "AppAddonManager", app_dir: str, service: str
) -> None:
    name = manager.get_app_name()
    manager.set_config(
        f"service.{service}",
        {
            "host": f"{name}_mysql",
            "name": f"{name}",
            "password": string_random_password(),
            "port": 3306,
            "user": "root",
        },
    )

    manager.set_config(
        ["structure", "schema", APP_DIR_APP_DATA_NAME],
        {
            "type": "dir",
            "schema": {
                service: {
                    "type": "dir",
                    "schema": {
                        "dumps": {
                            "type": "dir",
                            "schema": {
                                "db.latest.zip": {"type": "file", "remote": "push"}
                            },
                        }
                    },
                },
            },
        },
        when_exist=DICT_ITEM_EXISTS_ACTION_MERGE,
    )
