from src.core.CommandRequest import CommandRequest
from src.const.globals import KERNEL_RENDER_MODE_CLI
from src.core.response.AbstractResponse import AbstractResponse


class FunctionResponse(AbstractResponse):
    def __init__(self, kernel, function: callable):
        super().__init__(kernel)

        self.function = function

    def render_content(self,
               request: CommandRequest,
               render_mode: str = KERNEL_RENDER_MODE_CLI,
               args: dict = None) -> AbstractResponse:
        response = self.function(
            **(args or {})
        )

        if response is not None:
            self.output_bag.append(response)

        return self
