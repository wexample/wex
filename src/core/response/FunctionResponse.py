from src.const.globals import KERNEL_RENDER_MODE_CLI
from src.core.response.AbstractResponse import AbstractResponse


class FunctionResponse(AbstractResponse):
    def __init__(self, kernel, function: callable):
        super().__init__(kernel)

        self.function = function

    def render(self, render_mode: str = KERNEL_RENDER_MODE_CLI, args: dict = None) -> str | int | bool | None:
        return self.function(
            args
        )
