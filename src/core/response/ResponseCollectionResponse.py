from src.core.CommandRequest import CommandRequest
from src.const.globals import KERNEL_RENDER_MODE_CLI
from src.core.response.AbstractResponse import AbstractResponse


class ResponseCollectionResponse(AbstractResponse):
    def __init__(self, kernel, collection: list):
        super().__init__(kernel)

        self.collection = collection

    def render_content(
            self,
            request: CommandRequest,
            render_mode: str = KERNEL_RENDER_MODE_CLI,
            args: dict = None) -> AbstractResponse:

        for response in self.collection:
            self.output_bag.append(
                response.render_content(
                    request,
                    render_mode,
                    args,
                )
            )

        return self
