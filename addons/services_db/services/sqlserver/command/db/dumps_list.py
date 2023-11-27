import os.path
from glob import glob
from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from addons.app.helper.db import get_db_service_dumps_path
from src.const.globals import COMMAND_TYPE_SERVICE

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="List dumps", command_type=COMMAND_TYPE_SERVICE)
def sqlserver__db__dumps_list(manager: 'AppAddonManager', app_dir: str, service: str):
    dumps_dir = get_db_service_dumps_path(manager, service)

    # Search for .zip and .sql files
    search_patterns = ['*.zip', '*.bak']
    dump_files = []

    for pattern in search_patterns:
        dump_files.extend(glob(os.path.join(dumps_dir, pattern)))

    # Get the base names
    return dump_files
