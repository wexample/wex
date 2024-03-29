from typing import TYPE_CHECKING

from src.decorator.alias import alias
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from src.decorator.option import option

if TYPE_CHECKING:
    from src.const.types import KernelRegistry
    from src.core.Kernel import Kernel


@alias("rebuild")
@as_sudo()
@command(help="Rebuild core registry")
@option(
    "--test",
    "-t",
    is_flag=True,
    default=False,
    help="Register also commands marked as only for testing",
)
@option("--write", "-w", type=bool, default=True, help="Write registry file")
def core__registry__build(
    kernel: "Kernel", test: bool = False, write: bool = True
) -> "KernelRegistry":
    return kernel.registry_structure.build(test=test, write=write)
