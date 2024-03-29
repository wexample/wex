import os
from typing import TYPE_CHECKING

from addons.system.command.own.this import system__own__this
from src.decorator.alias import alias
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from src.decorator.no_log import no_log
from src.decorator.option import option
from src.helper.dir import dir_empty_dir

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@alias("cleanup")
@as_sudo()
@no_log()
@command(help="Uninstall core")
@option(
    "--test",
    "-t",
    is_flag=True,
    default=False,
    help="Register also commands marked as only for testing",
)
def core__core__cleanup(kernel: "Kernel", test: bool = False) -> None:
    tmp_dir = kernel.get_or_create_path("tmp")
    # Do not hard remove "tmp" as it might be a mounted volume
    dir_empty_dir(tmp_dir)

    os.makedirs(os.path.dirname(tmp_dir), exist_ok=True)
    with open(os.path.join(tmp_dir, ".gitkeep"), "a"):
        pass

    kernel.registry_structure.build(test=test)

    # Reset perms
    kernel.run_function(system__own__this, {"path": kernel.directory.path})

    # Recreate empty folder as some running services may need it.
    kernel.get_or_create_path("task")
