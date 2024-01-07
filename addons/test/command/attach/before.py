from typing import TYPE_CHECKING

from addons.test.command.command.has_attached import test__command__has_attached
from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.attach import attach
from src.decorator.command import command

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@attach(position="before", command=test__command__has_attached)
@command(help="Description", command_type=COMMAND_TYPE_ADDON)
def test__attach__before(kernel: "Kernel") -> str:
    kernel.io.log(f"Running BEFORE")
    return "BEFORE"
