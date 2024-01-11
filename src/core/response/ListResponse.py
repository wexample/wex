import os
from typing import TYPE_CHECKING

from src.const.globals import KERNEL_RENDER_MODE_JSON, KERNEL_RENDER_MODE_TERMINAL
from src.const.types import (
    OptionalCoreCommandArgsDict,
    ResponsePrintType,
    StringKeysDict,
)
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse
from src.core.response.AbstractTerminalSectionResponse import (
    AbstractTerminalSectionResponse,
)

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class ListResponse(AbstractTerminalSectionResponse):
    def __init__(
        self,
        kernel: "Kernel",
        list_data: StringKeysDict,
        default_render_mode: str = KERNEL_RENDER_MODE_JSON,
    ) -> None:
        super().__init__(kernel, default_render_mode)

        self.list_data: StringKeysDict = list_data

    def render_content(
        self,
        request: CommandRequest,
        render_mode: str | None = None,
        args: OptionalCoreCommandArgsDict = None,
    ) -> AbstractResponse:
        self.output_bag.append(self.list_data)

        return self

    def print(
        self,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        interactive_data: bool = True,
    ) -> ResponsePrintType:
        data = self.output_bag[0]
        assert isinstance(data, list)

        render_mode = render_mode or self._default_render_mode

        if render_mode == KERNEL_RENDER_MODE_TERMINAL:
            return os.linesep.join(data)
        if render_mode == KERNEL_RENDER_MODE_JSON:
            print_dict = []
            for key in data:
                if isinstance(data[key], AbstractResponse):
                    print_dict.append(data[key].print(render_mode))
                else:
                    print_dict.append(data[key])
            return print_dict

        return None
