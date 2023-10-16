import os.path
from glob import glob

from src.core.Kernel import Kernel
from addons.app.helpers.db import get_db_service_dumps_path
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command


@command(help="Set database permissions")
@app_dir_option()
@service_option()
def postgres__db__dumps_list(kernel: Kernel, app_dir: str, service: str):
    dumps_dir = get_db_service_dumps_path(kernel, service)

    # Search for .zip and .sql files
    search_patterns = ['*.zip', '*.sql']
    dump_files = []

    for pattern in search_patterns:
        dump_files.extend(glob(os.path.join(dumps_dir, pattern)))

    # Get the base names
    return dump_files
