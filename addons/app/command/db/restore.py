import os
import zipfile
from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from addons.app.helper.db import get_db_service_dumps_path
from src.const.globals import (
    COMMAND_CHAR_SERVICE,
    COMMAND_SEPARATOR_ADDON,
    COMMAND_TYPE_SERVICE,
)
from src.core.command.resolver.ServiceCommandResolver import ServiceCommandResolver
from src.decorator.option import option
from src.helper.dict import dict_get_item_by_path, dict_sort_values
from src.helper.file import file_delete_file_or_dir, file_path_has_no_extension
from src.helper.prompt import prompt_choice

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Restore a database dump", should_run=True)
@option("--file-path", "-f", type=str, required=False, help="Force file path")
def app__db__restore(
    manager: "AppAddonManager", app_dir: str, file_path: str | None = None
) -> None:
    kernel = manager.kernel

    # There is a probable mismatch between container / service names
    # but for now each service have only one container.
    service = manager.get_config("docker.main_db_container", required=True)
    assert isinstance(service, str)

    if not service:
        kernel.io.error("Missing db container")

    if not file_path:
        dumps = kernel.run_command(
            f"{COMMAND_CHAR_SERVICE}{service}{COMMAND_SEPARATOR_ADDON}db/dumps-list",
            {
                "app-dir": app_dir,
                "service": service,
            },
        ).first()

        dumps_dict = {os.path.basename(file): file for file in dumps}
        dumps_dict = dict_sort_values(dumps_dict)

        dump_file_name = prompt_choice(
            "Please select a dump to restore", list(dumps_dict)
        )

        if not dump_file_name:
            return

        file_path = dumps_dict[dump_file_name]

    is_zip = file_path.endswith(".zip")
    if os.path.exists(file_path) and is_zip:
        manager.log("Unpacking...")
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(get_db_service_dumps_path(manager, service))

        file_path = file_path.replace(".zip", "")

    if file_path_has_no_extension(file_path):
        service_resolver = kernel.get_command_resolver(COMMAND_TYPE_SERVICE)
        assert isinstance(service_resolver, ServiceCommandResolver)

        registry_data = service_resolver.get_registry_data()
        extension = dict_get_item_by_path(
            registry_data[service], "config.db.dump_extension", None
        )

        if not extension:
            return

        file_path += "." + extension

    if not os.path.exists(file_path):
        manager.kernel.io.error(f"Dump file not found: {file_path}")
        return

    manager.log("Restoring...")

    file_name = os.path.basename(file_path)
    kernel.run_command(
        f"{COMMAND_CHAR_SERVICE}{service}{COMMAND_SEPARATOR_ADDON}db/restore",
        {"app-dir": app_dir, "service": service, "file-name": file_name},
    ).first()

    if is_zip:
        file_delete_file_or_dir(file_path)

    kernel.io.message("Restoration complete")
