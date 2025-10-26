from __future__ import annotations

from typing import TYPE_CHECKING, cast
from addons.app.decorator.app_command import app_command

from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager
    from src.const.types import StringKeysDict


@app_command(help="Exec a command on services and local app")
@option("--hook", "-h", type=str, required=True, help="Hook name")
@option("--arguments", "-args", type=str, required=False, help="Hook name")
def app__hook__exec(
    manager: AppAddonManager, hook: str, arguments: str, app_dir: str | None = None
) -> StringKeysDict:
    from src.const.types import StringKeysDict
    from src.const.globals import COMMAND_CHAR_APP, VERBOSITY_LEVEL_MAXIMUM
    from wexample_helpers.helpers.args import args_parse_dict
    from addons.app.command.services.exec import app__services__exec

    arguments_dict = args_parse_dict(arguments)

    manager.kernel.io.log(f"Hooking : {hook}", verbosity=VERBOSITY_LEVEL_MAXIMUM)

    arguments_dict["app-dir"] = app_dir

    results = manager.kernel.run_function(
        app__services__exec,
        {
            "app-dir": app_dir,
            "arguments": arguments_dict,
            "hook": hook,
        },
    ).first()

    results[COMMAND_CHAR_APP] = manager.kernel.run_command(
        COMMAND_CHAR_APP + hook, arguments_dict, quiet=True
    )

    return cast(StringKeysDict, results)
