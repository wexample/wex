import os
import zipfile
from typing import TYPE_CHECKING, Optional, cast

from addons.app.command.remote.push import app__remote__push
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_CHAR_SERVICE, COMMAND_SEPARATOR_ADDON
from src.core.command.ScriptCommand import ScriptCommand
from src.decorator.attach import attach
from src.decorator.option import option
from src.helper.file import (
    file_build_date_time_name,
    file_create_symlink,
    file_delete_file_or_dir,
)

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@attach(
    position="before",
    command=cast(ScriptCommand, app__remote__push),
    pass_args=["app_dir"],
)
@app_command(help="Create a database dump", should_run=True)
@option("--file-name", "-fn", type=str, required=False, help="Output file name")
@option("--zip", "-z", type=bool, required=False, default=True, help="Zip output file")
@option("--tag", "-t", type=str, required=False, help="Add tag as suffix")
def app__db__dump(
    manager: "AppAddonManager",
    app_dir: str,
    file_name: str | None = None,
    zip: bool = True,
    tag: str | None = None,
) -> Optional[str]:
    if not manager.has_config("docker.main_db_container"):
        return None

    env = manager.get_env()
    name = manager.get_app_name()

    # Determine dump file name
    if file_name:
        dump_file_name = file_name
    else:
        dump_file_name = f"{env}-{name}-{file_build_date_time_name()}"
        if tag:
            dump_file_name += f"-{tag}"

    manager.log(f"Exporting dump to {dump_file_name}")

    # There is a probable mismatch between container / service names
    # but for now each service have only one container.
    service = manager.get_config("docker.main_db_container").get_str()

    output_path = dump_path = str(
        manager.kernel.run_command(
            f"{COMMAND_CHAR_SERVICE}{service}{COMMAND_SEPARATOR_ADDON}db/dump",
            {"app-dir": app_dir, "service": service, "file-name": dump_file_name},
        ).first()
    )

    if dump_path and os.path.exists(dump_path):
        if zip:
            manager.log("Creating zip file")
            zip_path = dump_path + ".zip"

            with zipfile.ZipFile(f"{zip_path}", "w") as zipf:
                zipf.write(dump_path, os.path.basename(dump_path))

            # Remove original dump file
            file_delete_file_or_dir(dump_path)
            output_path = zip_path

            # Create symlink to zip
            zip_symlink_path = f"{os.path.dirname(dump_path)}/db.latest.zip"
            manager.log(f"Creating zip symlink to {zip_symlink_path}")
            file_create_symlink(zip_path, zip_symlink_path)

        manager.kernel.io.message("Dump created at " + output_path)

        # Create symlink
        symlink_path = f"{os.path.dirname(dump_path)}/db.latest"
        manager.log(f"Creating zip symlink to {symlink_path}")
        file_create_symlink(output_path, symlink_path)

        return output_path

    return None
