from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.command import command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Description", command_type=COMMAND_TYPE_ADDON)
def test__attach__before(kernel: "Kernel") -> str:
    return "BEFORE"
