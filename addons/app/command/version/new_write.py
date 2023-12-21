from src.decorator.option import option
from typing import TYPE_CHECKING, Optional
from addons.default.command.version.increment import default__version__increment
from src.const.globals import CORE_COMMAND_NAME
from src.helper.core import core_kernel_get_version
from addons.app.decorator.app_command import app_command

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Build a new version of current app")
@option(
    "--version",
    "-v",
    type=str,
    required=False,
    help="New version number, auto generated if missing",
)
def app__version__new_write(
    manager: "AppAddonManager",
    app_dir: str,
    version: Optional[str] = None,
) -> str:
    kernel = manager.kernel

    if version:
        new_version = version
    else:
        new_version = kernel.run_function(
            default__version__increment,
            {"version": manager.get_config("global.version").get_str()},
        ).print_wrapped_str()

    # Save new version
    kernel.io.log(f"New app version : {new_version}")

    manager.set_config("global.version", new_version)
    manager.set_config(
        f"{CORE_COMMAND_NAME}.version", core_kernel_get_version(kernel)
    )

    kernel.run_command(".version/build", quiet=True)
    print('....')
    return new_version
