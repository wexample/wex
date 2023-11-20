import os.path
from glob import glob

from addons.app.helper.db import get_db_service_dumps_path
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="List dumps", command_type=COMMAND_TYPE_SERVICE, should_run=True)
def mysql__db__dumps_list(kernel: 'Kernel', app_dir: str, service: str):
    dumps_dir = get_db_service_dumps_path(kernel, service)

    # Search for .zip and .sql files
    search_patterns = ['*.zip', '*.sql']
    dump_files = []

    for pattern in search_patterns:
        dump_files.extend(glob(os.path.join(dumps_dir, pattern)))

    # Get the base names
    return dump_files
