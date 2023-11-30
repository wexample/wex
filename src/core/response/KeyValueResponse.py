import os
from typing import TYPE_CHECKING

from src.const.globals import KERNEL_RENDER_MODE_JSON, KERNEL_RENDER_MODE_TERMINAL
from src.const.types import OptionalCoreCommandArgsDict, ResponsePrintType, StringKeysDict
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse
from src.core.response.AbstractTerminalSectionResponse import (
    AbstractTerminalSectionResponse,
)

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class KeyValueResponse(AbstractTerminalSectionResponse):
    def __init__(
        self, kernel: "Kernel", dictionary: StringKeysDict, title: str | None = None
    ) -> None:
        super().__init__(kernel, title)

        self.dictionary_data = dictionary

    def render_content(
        self,
        request: CommandRequest,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        args: OptionalCoreCommandArgsDict = None,
    ) -> AbstractResponse:
        if render_mode == KERNEL_RENDER_MODE_TERMINAL:
            # Calculate maximum key width for formatting
            max_key_width = max(len(str(key)) for key in self.dictionary_data.keys())

            # Pre-render the lines to calculate the section width
            # We create the entire line here for width calculation
            lines = [
                f"{str(key):<{max_key_width}} : {value}"
                for key, value in self.dictionary_data.items()
            ]

            # Find the largest width
            section_width = max(len(line) for line in lines)

            # Generate the CLI title with the section width
            output = self.render_cli_title(self.title, section_width)

            # Add pre-rendered key/value pairs to the output
            for line in lines:
                output += line + os.linesep

            self.output_bag.append(output)

        elif render_mode == KERNEL_RENDER_MODE_JSON:
            # For HTTP mode, we simply use the dictionary to be converted as JSON
            self.output_bag.append(self.dictionary_data)

        return self

    def print(
        self,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        interactive_data: bool = True,
    ) -> ResponsePrintType:
        if render_mode == KERNEL_RENDER_MODE_TERMINAL:
            return os.linesep.join(self.output_bag)
        elif render_mode == KERNEL_RENDER_MODE_JSON:
            return self.dictionary_data
        return None
