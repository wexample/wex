from src.const.globals import KERNEL_RENDER_MODE_CLI
from src.core.response.AbstractResponse import AbstractResponse


class StringResponse(AbstractResponse):
    def __init__(self, string: str):
        self.string: str = string

    def render(self, kernel, render_mode: str = KERNEL_RENDER_MODE_CLI) -> str:
        return self.string
