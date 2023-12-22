import os
from typing import TYPE_CHECKING, Optional

import click

from addons.app.decorator.app_command import app_command
from addons.app.helper.app import app_create_manager
from addons.default.command.version.parse import default__version__parse
from addons.default.helper.migration import (
    MIGRATION_MINIMAL_VERSION,
    migration_exec,
    migration_extract_version_from_file_name,
    migration_get_files,
    migration_version_guess,
)
from addons.default.helper.version import is_greater_than
from src.const.globals import CORE_COMMAND_NAME
from src.decorator.option import option
from src.helper.core import core_kernel_get_version

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Description", dir_required=False)
@option(
    "--from-version",
    "-f",
    type=str,
    required=False,
    help="Force initial version number",
)
@option(
    "--yes",
    "-y",
    type=bool,
    is_flag=True,
    required=False,
    help="Do not ask for confirmation",
)
def app__migration__migrate(
    manager: "AppAddonManager",
    app_dir: str | None = None,
    from_version: Optional[str] = None,
    yes: bool = False,
) -> None:
    kernel = manager.kernel
    app_dir = app_dir or os.getcwd() + os.sep
    manager = app_create_manager(kernel, app_dir)
    app_version_string: str | None

    if from_version:
        app_version_string = from_version
    elif manager.has_config(f"{CORE_COMMAND_NAME}.version"):
        app_version_string = manager.get_config(
            f"{CORE_COMMAND_NAME}.version"
        ).get_str()
    else:
        app_version_string = migration_version_guess(kernel, app_dir)

    app_version = kernel.run_function(
        default__version__parse, {"version": app_version_string}
    ).first()

    # Unable to parse version number.
    if not app_version:
        app_version_string = MIGRATION_MINIMAL_VERSION

        app_version = kernel.run_function(
            default__version__parse, {"version": app_version_string}
        ).first()

    if manager.has_config("global.name"):
        app_name = manager.get_config("global.name").get_str()
    else:
        app_name = os.path.basename(os.path.normpath(app_dir))

    if not yes and not click.confirm(
        f"Are you ready to migrate {app_name} from version {app_version_string}",
        default=True,
    ):
        return

    # Create an empty config
    if not manager._config:
        # Only create config but do not save it
        # until migration is completed
        manager._config = manager.create_config(app_name)

    kernel.io.log(f"Current version defined as {app_version_string}")

    for migration_file in migration_get_files(kernel):
        migration_version_string = migration_extract_version_from_file_name(
            migration_file
        )

        if migration_version_string:
            migration_version = kernel.run_function(
                default__version__parse, {"version": migration_version_string}
            ).first()

            if is_greater_than(migration_version, app_version):
                kernel.io.log(f"Migrating to {migration_version_string}")

                migration_exec(kernel, migration_version_string, "migration", [manager])

                manager.set_config(
                    f"{CORE_COMMAND_NAME}.version", migration_version_string
                )

                app_version = migration_version

    manager.set_config(f"{CORE_COMMAND_NAME}.version", core_kernel_get_version(kernel))
    kernel.io.message(f"Migration complete")
