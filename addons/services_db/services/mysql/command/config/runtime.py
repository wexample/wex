import os
from typing import TYPE_CHECKING

from addons.app.const.app import APP_DIR_TMP
from addons.app.decorator.app_command import app_command
from addons.services_db.const.mysql import MYSQL_CONF_FILE
from src.const.globals import COMMAND_TYPE_SERVICE
from src.helper.file import DICT_ITEM_EXISTS_ACTION_ABORT

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Set runtime configuration", command_type=COMMAND_TYPE_SERVICE)
def mysql__config__runtime(
    manager: "AppAddonManager", app_dir: str, service: str
) -> None:
    # Set db as main database.
    manager.set_runtime_config(
        f"db.main",
        manager.get_config(f"service.{service}.name").get_str(),
        DICT_ITEM_EXISTS_ACTION_ABORT,
    )

    db_connection_file = os.path.join(app_dir, APP_DIR_TMP, MYSQL_CONF_FILE)

    # Write the MySQL configuration
    with open(db_connection_file, "w") as f:
        user = manager.get_config(f"service.{service}.user").get_str()
        password = manager.get_config(f"service.{service}.password").get_str()

        f.write(f"[client]{os.linesep}")
        f.write(f'user = "{user}"{os.linesep}')
        f.write(f'password = "{password}"{os.linesep}')

    # Change file permissions to 644
    os.chmod(db_connection_file, 0o644)
