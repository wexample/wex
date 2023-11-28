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


class DictResponse(AbstractTerminalSectionResponse):
    def __init__(
        self,
        kernel: "Kernel",
        dictionary: StringKeysDict,
        cli_render_mode: str = KERNEL_RENDER_MODE_JSON,
    ) -> None:
        super().__init__(kernel)

        self.cli_render_mode = cli_render_mode
        self.dictionary_data: StringKeysDict = dictionary

    def get_render_mode(self, render_mode: str | None = None) -> str:
        if render_mode:
            return render_mode

        return self.cli_render_mode

    def render_content(
        self,
        request: CommandRequest,
        render_mode: str | None = None,
        args: OptionalCoreCommandArgsDict = None,
    ) -> AbstractResponse:
        render_mode = self.get_render_mode(render_mode)

        # For HTTP mode, we simply use the dictionary to be converted as JSON
        self.output_bag.append(self.dictionary_data)

        self.render_content_multiple(
            self.dictionary_data.values(), request, render_mode, args
        )

        return self

    def print(
        self,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        interactive_data: bool = True,
    ) -> ResponsePrintType:
        data = self.output_bag[0]
        render_mode = self.get_render_mode(render_mode)

        if render_mode == KERNEL_RENDER_MODE_TERMINAL:
            print_string = []

            for key in data:
                if isinstance(data[key], AbstractResponse):
                    print_string.append(data[key].print(render_mode))
                else:
                    print_string.append(key + ": " + str(data[key]))

            return os.linesep.join(print_string)
        if render_mode == KERNEL_RENDER_MODE_JSON:
            print_dict = {}
            for key in data:
                if isinstance(data[key], AbstractResponse):
                    print_dict[key] = data[key].print(render_mode)
                else:
                    print_dict[key] = data[key]
            return print_dict

        return None
