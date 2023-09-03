from src.const.globals import KERNEL_RENDER_MODE_CLI
from src.core.response.AbstractResponse import AbstractResponse


class ExecThreadResponse(AbstractResponse):
    def __init__(self, thread: list):
        self.thread: list = thread

    def render(self, kernel, render_mode: str = KERNEL_RENDER_MODE_CLI) -> str | int | bool | None:
        # TODO
        return len(self.thread)
