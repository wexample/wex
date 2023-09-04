from src.const.globals import KERNEL_RENDER_MODE_CLI
from src.core.response.AbstractResponse import AbstractResponse


class FunctionResponse(AbstractResponse):
    def __init__(self, kernel, function: list):
        super().__init__(kernel)

        self.function = function

    def render(self, kernel, render_mode: str = KERNEL_RENDER_MODE_CLI):
        return self.function
