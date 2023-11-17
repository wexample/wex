from src.core.response.HiddenResponse import HiddenResponse
from src.decorator.command import command
from src.core import Kernel
from src.const.globals import COMMAND_TYPE_ADDON


@command(help="Return a hidden value", command_type=COMMAND_TYPE_ADDON)
def test__return_type__hidden(kernel: Kernel):
    # Internal usage only
    return HiddenResponse(kernel, 'SHOULD_NEVER_BEEN_DISPLAYED')
