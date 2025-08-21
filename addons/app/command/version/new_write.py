from typing import TYPE_CHECKING, Optional

import git

from addons.app.decorator.app_command import app_command
from addons.default.command.version.increment import \
    default__version__increment
from src.const.globals import VERSION_DEFAULT
from src.decorator.option import option

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
@option(
    "--branch",
    "-b",
    type=bool,
    default=True,
    help="Create a new branch",
)
def app__version__new_write(
    manager: "AppAddonManager",
    app_dir: str,
    version: Optional[str] = None,
    branch: bool = True,
) -> str:
    kernel = manager.kernel

    if version:
        new_version = version
    else:
        new_version = kernel.run_function(
            default__version__increment,
            {
                "version": manager.get_config(
                    "global.version", VERSION_DEFAULT
                ).get_str()
            },
        ).print_wrapped_str()

    if branch:
        repo = git.Repo(search_parent_directories=True)
        new_branch_name = f"version-{new_version}"
        branch_exists = any((heads.name == new_branch_name for heads in repo.heads))

        if not branch_exists:
            repo.git.checkout("HEAD", b=new_branch_name)
            kernel.io.success(f"Branch created : {new_branch_name}")
        else:
            repo.git.checkout(new_branch_name)
            kernel.io.success(f"Branch exists : {new_branch_name}")

    # Save new version
    kernel.io.log(f"New app version : {new_version}")

    manager.set_config("global.version", new_version)

    return new_version
