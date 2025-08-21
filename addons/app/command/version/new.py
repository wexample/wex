from typing import TYPE_CHECKING, Optional

from addons.app.command.version.new_commit import app__version__new_commit
from addons.app.command.version.new_write import app__version__new_write
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Description", command_type=COMMAND_TYPE_ADDON)
@option(
    "--version",
    "-v",
    type=str,
    required=False,
    help="New version number, auto generated if missing",
)
def app__version__new(
    manager: "AppAddonManager", app_dir: str, version: Optional[str] = None
) -> str:
    new_version = manager.kernel.run_function(
        app__version__new_write,
        {
            "version": version,
            "app_dir": app_dir,
        },
    ).first()

    manager.kernel.run_function(
        app__version__new_commit,
        {
            "app_dir": app_dir,
        },
    )

    return str(new_version)
