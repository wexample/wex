from typing import TYPE_CHECKING, Optional, cast

from addons.app.command.services.exec import app__services__exec
from addons.app.decorator.app_command import app_command
from src.const.types import StringKeysDict
from src.const.globals import COMMAND_CHAR_APP
from src.decorator.option import option
from src.helper.args import args_parse_one

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Exec a command on services and local app")
@option("--hook", "-h", type=str, required=True, help="Hook name")
@option("--arguments", "-args", type=str, required=False, help="Hook name")
def app__hook__exec(
        manager: "AppAddonManager",
        hook: str,
        arguments: str,
        app_dir: Optional[str] = None
) -> StringKeysDict:
    arguments_dict = cast(StringKeysDict, args_parse_one(arguments) or {})

    manager.log(f"Hooking : {hook}")

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
