from src.const.globals import KERNEL_RENDER_MODE_CLI, KERNEL_RENDER_MODE_COMMAND
from src.core.response.AbstractResponse import AbstractResponse


class FunctionResponse(AbstractResponse):
    def __init__(self, kernel, function: callable):
        super().__init__(kernel)

        self.function = function

    def render(self, render_mode: str = KERNEL_RENDER_MODE_CLI) -> str | int | bool | None:
        if render_mode is KERNEL_RENDER_MODE_COMMAND:
            return self.function

        return self.function()
