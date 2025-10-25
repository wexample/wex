from __future__ import annotations

from typing import TYPE_CHECKING

from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.command import command

if TYPE_CHECKING:
    from src.utils.kernel import Kernel
    from src.core.response.KeyValueResponse import KeyValueResponse


@command(help="Return a key / value response", command_type=COMMAND_TYPE_ADDON)
def test__return_type__key_value(kernel: Kernel) -> KeyValueResponse:
    from src.core.response.KeyValueResponse import KeyValueResponse
    return KeyValueResponse(kernel, {"str": "lorem", "int": 123, "bool": True})
