from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Return connexion info", command_type=COMMAND_TYPE_SERVICE)
@option(
    "--protocol", "-p", type=str, required=False, default="postgresql", help="Protocol"
)
@option("--database", "-d", type=str, required=False, help="Database name")
def postgres__db__connect(
    manager: "AppAddonManager",
    app_dir: str,
    service: str,
    protocol: str = "postgresql",
    database: str | None = None,
) -> str:
    user = manager.get_config(f"service.{service}.user").get_str()
    password = manager.get_config(f"service.{service}.password").get_str()
    name = database or manager.get_config(f"service.{service}.name").get_str()

    return f'{protocol}://{user}:"{password}"@localhost/{name}'
