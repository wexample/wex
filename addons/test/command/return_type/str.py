from typing import TYPE_CHECKING

from src.decorator.command import command
from src.decorator.option import option

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Return a string")
@option("--arg", "-a", type=str, required=True, help="Argument")
def test__return_type__str(kernel: "Kernel", arg: str) -> str:
    return str(arg)
