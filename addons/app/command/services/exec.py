from typing import TYPE_CHECKING

from wexample_helpers.helpers.args import args_parse_dict

from addons.app.decorator.app_command import app_command
from src.const.globals import (COMMAND_CHAR_SERVICE, COMMAND_SEPARATOR_ADDON,
                               VERBOSITY_LEVEL_MAXIMUM)
from src.const.types import StringKeysDict
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Execute a command for all installed services")
@option("--hook", "-h", type=str, required=True, help="Hook name")
@option("--arguments", "-args", type=str, required=False, help="Arguments")
def app__services__exec(
    manager: "AppAddonManager", app_dir: str, hook: str, arguments: str
) -> StringKeysDict:
    output = {}

    arguments_dict = args_parse_dict(arguments)
    services = manager.get_services()

    for service in services:
        arguments_dict_copy = arguments_dict.copy()
        arguments_dict_copy["service"] = service

        command_name = f"{COMMAND_CHAR_SERVICE}{service}{COMMAND_SEPARATOR_ADDON}{hook}"

        manager.kernel.io.log(command_name, verbosity=VERBOSITY_LEVEL_MAXIMUM)

        output[f"{COMMAND_CHAR_SERVICE}{service}"] = manager.kernel.run_command(
            command_name, arguments_dict_copy, quiet=True
        )

    return output
