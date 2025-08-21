import os
from typing import TYPE_CHECKING

from src.const.globals import (KERNEL_RENDER_MODE_JSON,
                               KERNEL_RENDER_MODE_TERMINAL)
from src.const.types import (AnyList, OptionalCoreCommandArgsDict,
                             ResponsePrintType)
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse
from src.core.response.AbstractTerminalSectionResponse import \
    AbstractTerminalSectionResponse

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


class ListResponse(AbstractTerminalSectionResponse):
    def __init__(
        self,
        kernel: "Kernel",
        list_data: AnyList,
        default_render_mode: str = KERNEL_RENDER_MODE_JSON,
    ) -> None:
        super().__init__(kernel, default_render_mode)

        self.list_data: AnyList = list_data

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

        render_mode = (
            render_mode or self._default_render_mode or KERNEL_RENDER_MODE_TERMINAL
        )

        if render_mode == KERNEL_RENDER_MODE_TERMINAL:
            return os.linesep.join(data)
        if render_mode == KERNEL_RENDER_MODE_JSON:
            print_dict = []
            for value in data:
                if isinstance(value, AbstractResponse):
                    print_dict.append(value.print(render_mode))
                else:
                    print_dict.append(value)
            return print_dict

        return None
