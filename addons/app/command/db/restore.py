import os
import zipfile

from addons.app.AppAddonManager import AppAddonManager
from addons.app.decorator.app_should_run import app_should_run
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.helpers.db import get_db_service_dumps_path
from src.helper.file import delete_file_or_dir
from src.helper.prompt import prompt_choice
from src.const.globals import COMMAND_CHAR_SERVICE, COMMAND_SEPARATOR_ADDON
from src.decorator.command import command
from src.decorator.option import option
from src.core import Kernel


@command(help="Restore a database dump")
@app_should_run
@app_dir_option()
@option('--file-path', '-f', type=str, required=False, help="Force file path")
def app__db__restore(kernel: Kernel, app_dir: str, file_path: str | None = None):
    manager: AppAddonManager = kernel.addons['app']

    # There is a probable mismatch between container / service names
    # but for now each service have only one container.
    service = manager.get_config('docker.main_db_container')

    if not file_path:
        dumps = kernel.run_command(
            f'{COMMAND_CHAR_SERVICE}{service}{COMMAND_SEPARATOR_ADDON}db/dumps-list',
            {
                'app-dir': app_dir,
                'service': service,
            }
        ).first()

        dumps_dict = {os.path.basename(file): file for file in dumps}

        dump_file_name = prompt_choice(
            'Please select a dump to restore',
            list(dumps_dict)
        )

        file_path = dumps_dict[dump_file_name]

    if not os.path.exists(file_path):
        manager.log(f"File not found: {file_path}")
        return

    is_zip = file_path.endswith('.zip')
    if is_zip:
        manager.log("Unpacking...")
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(
                get_db_service_dumps_path(kernel, service)
            )

        file_path = os.path.basename(file_path).replace('.zip', '')

    manager.log("Restoring...")

    kernel.run_command(
        f'{COMMAND_CHAR_SERVICE}{service}{COMMAND_SEPARATOR_ADDON}db/restore',
        {
            'app-dir': app_dir,
            'service': service,
            'file-name': file_path
        }
    ).first()

    if is_zip:
        delete_file_or_dir(get_db_service_dumps_path(kernel, service) + '/' + file_path)

    kernel.io.message('Restoration complete')
