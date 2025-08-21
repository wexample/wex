from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from src.core.response.AbstractResponse import AbstractResponse
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(
    help="Destroy database", command_type=COMMAND_TYPE_SERVICE, should_run=True
)
@option("--database", "-d", type=str, required=False, help="Database name")
@option(
    "--recreate",
    "-r",
    type=bool,
    required=False,
    default=True,
    help="Recreate an empty database",
)
def postgres__db__destroy(
    manager: "AppAddonManager",
    app_dir: str,
    service: str,
    database: str | None = None,
    recreate: bool = True,
) -> None:
    from addons.app.command.app.exec import app__app__exec
    from addons.services_db.services.postgres.command.db.connect import \
        postgres__db__connect

    fallback_database = "postgres"

    def run_psql_command(command: str, message: str) -> AbstractResponse:
        manager.log(message)
        result = manager.kernel.run_function(
            app__app__exec,
            {
                "app-dir": app_dir,
                "container-name": service,
                "command": [
                    "psql",
                    manager.kernel.run_function(
                        postgres__db__connect,
                        {
                            "database": fallback_database,
                            "app-dir": app_dir,
                            "service": service,
                        },
                        type=COMMAND_TYPE_SERVICE,
                    ).first(),
                    "-c",
                    f'"{command}"',
                ],
                "sync": True,
            },
        )
        result.print()
        return result

    # Terminate connections to the database
    terminate_command = f"SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '{database}' AND pid <> pg_backend_pid();"
    run_psql_command(
        terminate_command, f'Terminating connections to the database "{database}"'
    )

    # Drop the database
    drop_command = f'DROP DATABASE IF EXISTS "{database}";'
    run_psql_command(drop_command, f'Dropping the database "{database}"')

    # Create the database if needed
    if recreate:
        create_command = f'CREATE DATABASE "{database}";'
        run_psql_command(create_command, f'Creating an empty database "{database}"')
