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

        if render_mode == KERNEL_RENDER_MODE_CLI:
            # Calculate maximum key width for formatting
            max_key_width = max(len(str(key)) for key in self.dictionary_data.keys())

            # Pre-render the lines to calculate the section width
            # We create the entire line here for width calculation
            lines = [f"{str(key):<{max_key_width}} : {value}" for key, value in self.dictionary_data.items()]

            # Find the largest width
            section_width = max(len(line) for line in lines)

            # Generate the CLI title with the section width
            output = self.render_cli_title(section_width)

            # Add pre-rendered key/value pairs to the output
            for line in lines:
                output += line + '\n'

            self.output_bag.append(output)

        elif render_mode == KERNEL_RENDER_MODE_HTTP:
            # For HTTP mode, we simply convert the dictionary to JSON
            self.output_bag.append(json.dumps(self.dictionary_data))

        return self
