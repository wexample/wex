import os
from typing import cast

from src.const.globals import KERNEL_RENDER_MODE_JSON, KERNEL_RENDER_MODE_TERMINAL
from src.const.types import JsonContent, OptionalCoreCommandArgsDict, ResponsePrintType
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse, ResponseCollection


class ResponseCollectionResponse(AbstractResponse):
    def __init__(self, kernel: "Kernel", collection: ResponseCollection) -> None:
        super().__init__(kernel)

        self.collection: ResponseCollection = collection

    def render_content(
        self,
        request: CommandRequest,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        args: OptionalCoreCommandArgsDict = None,
    ) -> AbstractResponse:
        self.render_content_multiple(self.collection, request, render_mode, args)

        return self

    def print(
        self,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        interactive_data: bool = True,
    ) -> ResponsePrintType:
        if render_mode == KERNEL_RENDER_MODE_TERMINAL:
            return os.linesep.join(super().print(render_mode, interactive_data))
        if render_mode == KERNEL_RENDER_MODE_JSON:
            data = []

            for response in self.collection:
                data.append(response.print(render_mode, interactive_data))

            return data

    def render_mode_json_wrap_data(self, value: ResponsePrintType) -> JsonContent:
        # Do not add extra json wrapping
        return cast(JsonContent, value)
