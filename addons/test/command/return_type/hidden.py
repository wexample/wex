from __future__ import annotations

from typing import TYPE_CHECKING

from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.command import command

if TYPE_CHECKING:
    from src.utils.kernel import Kernel
    from src.core.response.HiddenResponse import HiddenResponse


@command(help="Return a hidden value", command_type=COMMAND_TYPE_ADDON)
def test__return_type__hidden(kernel: Kernel) -> HiddenResponse:
    from src.core.response.HiddenResponse import HiddenResponse

    # Internal usage only
    return HiddenResponse(kernel, "SHOULD_NEVER_BEEN_DISPLAYED")
