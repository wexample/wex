from typing import TYPE_CHECKING

from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.command import command

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Validate the code of current application", command_type=COMMAND_TYPE_ADDON)
def app__code__check(kernel: "Kernel") -> None:
    """
    This method is a placeholder to allow local app command attachment.s
    """
    return None
