from typing import TYPE_CHECKING

from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.command import command

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Description", command_type=COMMAND_TYPE_ADDON)
def test__command__has_attached(kernel: "Kernel") -> str:
    return "OK"
