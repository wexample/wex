import os
import zipfile

from addons.app.AppAddonManager import AppAddonManager
from addons.app.helper.db import get_db_service_dumps_path
from src.helper.dict import dict_sort_values
from src.helper.file import file_delete_file_or_dir
from src.helper.prompt import prompt_choice
from src.const.globals import COMMAND_CHAR_SERVICE, COMMAND_SEPARATOR_ADDON
from src.decorator.option import option
from src.core import Kernel
from addons.app.decorator.app_command import app_command


@app_command(help="Restore a database dump", should_run=True)
@option('--file-path', '-f', type=str, required=False, help="Force file path")
def app__db__restore(kernel: Kernel, app_dir: str, file_path: str | None = None):
    manager: AppAddonManager = kernel.addons['app']

    # There is a probable mismatch between container / service names
    # but for now each service have only one container.
    service = manager.get_config(
        'docker.main_db_container',
        required=True
    )

    if not service:
        kernel.io.error('Missing db container')

    if not file_path:
        dumps = kernel.run_command(
            f'{COMMAND_CHAR_SERVICE}{service}{COMMAND_SEPARATOR_ADDON}db/dumps-list',
            {
                'app-dir': app_dir,
                'service': service,
            }
        ).first()

        dumps_dict = {os.path.basename(file): file for file in dumps}
        dumps_dict = dict_sort_values(dumps_dict)

        dump_file_name = prompt_choice(
            'Please select a dump to restore',
            list(dumps_dict)
        )

        if not dump_file_name:
            return

        file_path = dumps_dict[dump_file_name]

    if not file_path or not os.path.exists(file_path):
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
        file_delete_file_or_dir(get_db_service_dumps_path(kernel, service) + '/' + file_path)

    kernel.io.message('Restoration complete')
