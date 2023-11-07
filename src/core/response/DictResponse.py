import json

from src.core.response.AbstractTerminalSectionResponse import AbstractTerminalSectionResponse
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse
from src.const.globals import KERNEL_RENDER_MODE_CLI, KERNEL_RENDER_MODE_HTTP


class DictResponse(AbstractTerminalSectionResponse):
    def __init__(self, kernel, dictionary: dict | None = None):
        super().__init__(kernel, dictionary)

        self.dictionary_data = {}

        if dictionary:
            self.set_dictionary(dictionary)

    def set_dictionary(self, dictionary_data):
        self.dictionary_data = dictionary_data

    def render_content(
            self,
            request: CommandRequest,
            render_mode: str = KERNEL_RENDER_MODE_CLI,
            args: dict = None) -> AbstractResponse:
        # For HTTP mode, we simply use the dictionary to be converted as JSON
        self.output_bag.append(self.dictionary_data)

        self.render_content_multiple(
            self.dictionary_data.values(),
            request,
            render_mode,
            args
        )

        return self

    def print(self, render_mode: str, interactive_data: bool = True):
        if render_mode == KERNEL_RENDER_MODE_CLI:
            return super().print(render_mode, interactive_data)[0]
        if render_mode == KERNEL_RENDER_MODE_HTTP:
            data = self.first()
            printed = {}
            for key in data:
                if isinstance(data[key], AbstractResponse):
                    printed[key] = data[key].print(render_mode)

            return json.dumps(printed)
