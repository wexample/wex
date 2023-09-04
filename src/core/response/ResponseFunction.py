from src.const.globals import KERNEL_RENDER_MODE_CLI
from src.core.response.AbstractResponse import AbstractResponse


class ResponseFunction(AbstractResponse):
    def __int__(self, kernel, function: list):
        super().__init__(kernel)

        self.function = function

    def render(self, kernel, render_mode: str = KERNEL_RENDER_MODE_CLI) -> str | int | bool | None:
        return 'FUNCTION'