from src.core.CommandRequest import CommandRequest
from src.const.globals import KERNEL_RENDER_MODE_TERMINAL
from src.core.response.AbstractResponse import AbstractResponse


class DefaultResponse(AbstractResponse):
    def __init__(self, kernel, content):
        super().__init__(kernel)
        self.content: str = content

    def render_content(
            self,
            request: CommandRequest,
            render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
            args: dict = None) -> AbstractResponse:
        self.output_bag.append(self.content)

        return self

    def print(self, render_mode: str = KERNEL_RENDER_MODE_TERMINAL, interactive_data: bool = True):
        return self.output_bag[0]
