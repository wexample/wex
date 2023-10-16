import os

from src.core.Kernel import Kernel
from src.decorator.command import command
from addons.app.const.app import APP_DIR_TMP
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from addons.app.AppAddonManager import AppAddonManager
from addons.services_db.const.mysql import MYSQL_CONF_FILE


@command(help="Set configuration")
@app_dir_option()
@service_option()
def mysql__config__runtime(kernel: Kernel, app_dir: str, service: str):
    manager: AppAddonManager = kernel.addons['app']
    # Set db as main database.
    manager.set_runtime_config(
        f'db.main',
        manager.get_config(f'service.{service}'),
        False
    )

    db_connection_file = os.path.join(
        app_dir,
        APP_DIR_TMP,
        MYSQL_CONF_FILE
    )

    # Write the MySQL configuration
    with open(db_connection_file, "w") as f:
        user = manager.get_config(f'service.{service}.user')
        password = manager.get_config(f'service.{service}.password')

        f.write("[client]\n")
        f.write(f'user = "{user}"\n')
        f.write(f'password = "{password}"\n')

    # Change file permissions to 644
    os.chmod(db_connection_file, 0o644)



