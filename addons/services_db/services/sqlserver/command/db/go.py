from typing import TYPE_CHECKING, Optional

from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(
    help="Enter in db console", command_type=COMMAND_TYPE_SERVICE, should_run=True
)
@option("--database", "-d", type=str, required=False, help="Database name")
def sqlserver__db__go(
    manager: "AppAddonManager",
    app_dir: str,
    service: str,
    database: Optional[str] = None,
)->str:
    user = manager.get_config(f"service.{service}.user")
    password = manager.get_config(f"service.{service}.password")
    name = database or manager.get_config(f"service.{service}.name")

    return (
        f'/opt/mssql-tools/bin/sqlcmd -S localhost -U {user} -P "{password}" -d {name}'
    )
