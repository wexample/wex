from typing import TYPE_CHECKING

from src.const.globals import COMMAND_TYPE_SERVICE
from src.decorator.option import option
from src.decorator.test_command import test_command

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


@test_command(command_type=COMMAND_TYPE_SERVICE)
@option("--option", "-o", is_flag=True, required=False, help="A first option as flag")
@option(
    "--another-option-second",
    "-aos",
    is_flag=True,
    required=False,
    help="Another option",
)
def test__demo_command__second(
    kernel: "Kernel",
    service: str,
    option: bool = False,
    another_option_second: bool = False,
) -> str:
    return "SECOND"
