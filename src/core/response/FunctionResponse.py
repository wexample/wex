from src.const.globals import KERNEL_RENDER_MODE_TERMINAL
from src.const.types import OptionalCoreCommandArgsDict, ResponsePrintType
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse


class FunctionResponse(AbstractResponse):
    def __init__(self, kernel, function: callable):
        super().__init__(kernel)

        self.function = function

    def render_content(
        self,
        request: CommandRequest,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        args: OptionalCoreCommandArgsDict = None,
    ) -> AbstractResponse:
        response = self.function(**(args or {}))

        response = request.resolver.wrap_response(response)

        # Propagate rendering
        response.render(
            request=request,
            render_mode=render_mode,
            args=args,
        )

        self.output_bag.append(response)

        return self

    def print(
        self,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        interactive_data: bool = True,
    ) -> ResponsePrintType:
        return self.output_bag[0].print()
