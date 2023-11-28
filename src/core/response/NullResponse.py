from abc import ABC

from src.const.globals import KERNEL_RENDER_MODE_TERMINAL
from src.const.types import OptionalCoreCommandArgsDict, ResponsePrintType
from src.core import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse


class NullResponse(AbstractResponse, ABC):
    def render_content(
        self,
        request: CommandRequest,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        args: OptionalCoreCommandArgsDict = None,
    ) -> None:
        self.output_bag.append(None)

    def print(
        self,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        interactive_data: bool = True,
    ) -> ResponsePrintType:
        if render_mode == KERNEL_RENDER_MODE_TERMINAL:
            return super().print(render_mode, interactive_data)
