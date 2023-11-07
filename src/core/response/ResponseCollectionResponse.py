import json

from src.core.CommandRequest import CommandRequest
from src.const.globals import KERNEL_RENDER_MODE_CLI, KERNEL_RENDER_MODE_HTTP
from src.core.response.AbstractResponse import AbstractResponse


class ResponseCollectionResponse(AbstractResponse):
    def __init__(self, kernel, collection: list):
        super().__init__(kernel)

        self.collection = collection

    def render_content(
            self,
            request: CommandRequest,
            render_mode: str = KERNEL_RENDER_MODE_CLI,
            args: dict = None) -> AbstractResponse:

        self.render_content_multiple(
            self.collection,
            request,
            render_mode,
            args
        )

        return self

    def print(self, render_mode: str, interactive_data: bool = True):
        if render_mode == KERNEL_RENDER_MODE_CLI:
            return "\n".join(
                super().print(render_mode, interactive_data)
            )
        if render_mode == KERNEL_RENDER_MODE_HTTP:
            data = []

            for response in self.collection:
                data.append(response.first())

            return json.dumps(data)
