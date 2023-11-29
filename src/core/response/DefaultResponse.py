from typing import TYPE_CHECKING, Any

from src.const.globals import KERNEL_RENDER_MODE_TERMINAL
from src.const.types import OptionalCoreCommandArgsDict, ResponsePrintType
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class DefaultResponse(AbstractResponse):
    def __init__(self, kernel: "Kernel", content: Any) -> None:
        super().__init__(kernel)
        self.content: Any = content

    def render_content(
        self,
        request: CommandRequest,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        args: OptionalCoreCommandArgsDict = None,
    ) -> AbstractResponse:
        self.output_bag.append(self.content)

        return self

    def print(
        self,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        interactive_data: bool = True,
    ) -> ResponsePrintType:
        return self.get_first_output_printable_value()
