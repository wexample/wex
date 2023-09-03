from src.const.globals import KERNEL_RENDER_MODE_CLI
from src.core.response.AbstractResponse import AbstractResponse


class DefaultResponse(AbstractResponse):
    def __init__(self, body: str):
        self.body: str = body

    def render(self, kernel, render_mode: str = KERNEL_RENDER_MODE_CLI) -> str | int | bool | None:
        return self.body
