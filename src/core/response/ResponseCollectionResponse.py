import os

from src.core.CommandRequest import CommandRequest
from src.const.globals import KERNEL_RENDER_MODE_TERMINAL, KERNEL_RENDER_MODE_JSON
from src.core.response.AbstractResponse import AbstractResponse


class ResponseCollectionResponse(AbstractResponse):
    def __init__(self, kernel, collection: list):
        super().__init__(kernel)

        self.collection = collection

    def render_content(
            self,
            request: CommandRequest,
            render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
            args: dict = None) -> AbstractResponse:

        self.render_content_multiple(
            self.collection,
            request,
            render_mode,
            args
        )

        return self

    def print(self, render_mode: str = KERNEL_RENDER_MODE_TERMINAL, interactive_data: bool = True):
        if render_mode == KERNEL_RENDER_MODE_TERMINAL:
            return os.linesep.join(
                super().print(render_mode, interactive_data)
            )
        if render_mode == KERNEL_RENDER_MODE_JSON:
            data = []

            for response in self.collection:
                data.append(response.print(render_mode, interactive_data))

            return data

    def render_mode_json_wrap_data(self, value):
        # Do not add extra json wrapping
        return value
