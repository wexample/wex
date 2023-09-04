from src.const.globals import KERNEL_RENDER_MODE_CLI
from src.core.response.AbstractResponse import AbstractResponse


class DefaultResponse(AbstractResponse):
    def __init__(self, kernel, body):
        super().__init__(kernel)
        self.body: str = body

    def render(self, render_mode: str = KERNEL_RENDER_MODE_CLI) -> str | int | bool | None:
        return self.body
