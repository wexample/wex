import os
from typing import Optional

from src.const.globals import (KERNEL_RENDER_MODE_JSON,
                               KERNEL_RENDER_MODE_TERMINAL)
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse
from src.core.response.AbstractTerminalSectionResponse import \
    AbstractTerminalSectionResponse


class DictResponse(AbstractTerminalSectionResponse):
    def __init__(self, kernel, dictionary: dict | None = None, cli_render_mode: str = KERNEL_RENDER_MODE_JSON):
        super().__init__(kernel, dictionary)

        self.dictionary_data = {}
        self.cli_render_mode = cli_render_mode

        if dictionary:
            self.set_dictionary(dictionary)

    def set_dictionary(self, dictionary_data):
        self.dictionary_data = dictionary_data

    def get_render_mode(self, render_mode: str | None = None):
        if render_mode:
            return render_mode

        return self.cli_render_mode

    def render_content(
            self,
            request: CommandRequest,
            render_mode: str | None = None,
            args: Optional[dict] = None) -> AbstractResponse:

        render_mode = self.get_render_mode(render_mode)

        # For HTTP mode, we simply use the dictionary to be converted as JSON
        self.output_bag.append(self.dictionary_data)

        self.render_content_multiple(
            self.dictionary_data.values(),
            request,
            render_mode,
            args
        )

        return self

    def print(self, render_mode: str = KERNEL_RENDER_MODE_TERMINAL, interactive_data: bool = True):
        data = self.output_bag[0]
        render_mode = self.get_render_mode(render_mode)

        if render_mode == KERNEL_RENDER_MODE_TERMINAL:
            printed = []

            for key in data:
                if isinstance(data[key], AbstractResponse):
                    printed.append(
                        data[key].print(
                            render_mode
                        )
                    )
                else:
                    printed.append(key + ': ' + str(data[key]))

            return os.linesep.join(printed)
        if render_mode == KERNEL_RENDER_MODE_JSON:
            printed = {}
            for key in data:
                if isinstance(data[key], AbstractResponse):
                    printed[key] = data[key].print(
                        render_mode
                    )
                else:
                    printed[key] = data[key]
            return printed
