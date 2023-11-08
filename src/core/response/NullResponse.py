from abc import ABC

from src.core import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse
from src.const.globals import KERNEL_RENDER_MODE_TERMINAL, KERNEL_RENDER_MODE_JSON


class NullResponse(AbstractResponse, ABC):
    def render_content(
            self,
            request: CommandRequest,
            render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
            args: dict = None) -> AbstractResponse:
        self.output_bag.append(None)

        return self

    def print(self, render_mode: str = KERNEL_RENDER_MODE_TERMINAL, interactive_data: bool = True):
        if render_mode == KERNEL_RENDER_MODE_TERMINAL:
            return super().print(
                render_mode,
                interactive_data
            )
        if render_mode == KERNEL_RENDER_MODE_JSON:
            return {}
