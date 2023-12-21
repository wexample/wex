from typing import TYPE_CHECKING

from git import Repo  # type: ignore

from addons.core.command.version.new_write import core__version__new_write
from addons.core.command.version.new_commit import core__version__new_commit
from addons.default.const.default import UPGRADE_TYPE_MINOR
from src.decorator.command import command
from src.decorator.option import option

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Build a new version of current core, or commit new version changes")
@option("--type", "-t", type=str, required=False, help="Type of update")
def core__version__new(kernel: "Kernel", type: str = UPGRADE_TYPE_MINOR) -> str:
    new_version = kernel.run_function(
        core__version__new_write,
        {
            "type": type,
        },
    ).first()

    kernel.run_function(
        core__version__new_commit
    )

    return str(new_version)
