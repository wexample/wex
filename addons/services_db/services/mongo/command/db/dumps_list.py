import os.path
from glob import glob

from addons.app.helpers.db import get_db_service_dumps_path
from src.core.Kernel import Kernel
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE


@app_command(help="List dumps", command_type=COMMAND_TYPE_SERVICE)
def mongo__db__dumps_list(kernel: Kernel, app_dir: str, service: str):
    dumps_dir = get_db_service_dumps_path(kernel, service)

    # Search for .zip and .sql files
    search_patterns = ['*.zip', '*.bson']
    dump_files = []

    for pattern in search_patterns:
        dump_files.extend(glob(os.path.join(dumps_dir, pattern)))

    # Get the base names
    return dump_files
