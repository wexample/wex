from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Destroy database", command_type=COMMAND_TYPE_SERVICE, should_run=True)
@option("--database", "-d", type=str, required=False, help="Database name")
@option("--recreate", "-r", type=bool, required=False, default=True, help="Recreate an empty database")
def mongo__db__destroy(
    manager: "AppAddonManager",
    app_dir: str,
    service: str,
    database: str | None = None,
    recreate: bool = True
) -> None:
    # TODO
    return
