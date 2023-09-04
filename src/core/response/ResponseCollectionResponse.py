import inspect

from src.const.error import ERR_UNEXPECTED
from src.const.globals import KERNEL_RENDER_MODE_CLI
from src.core.response.AbstractResponse import AbstractResponse


class ResponseCollectionResponse(AbstractResponse):
    def __init__(self, kernel, collection: list):
        super().__init__(kernel)

        self.collection = collection

    def error(self, message_end):
        request = self.kernel.current_request

        self.kernel.error(
            ERR_UNEXPECTED,
            {
                'error': f'Command "{request.command}" returns a {str(type(self))} response, {message_end}'
            }
        )

    def render(self, render_mode: str = KERNEL_RENDER_MODE_CLI) -> str | int | bool | None:
        request = self.kernel.current_request

        if not hasattr(request.function.callback, 'response_collection'):
            self.error(f'but has no @response_collection decorator')

        sig = inspect.signature(request.function.callback)
        if not 'response_collection_step' in sig.parameters:
            param = sig.parameters['response_collection_step']
            if param.annotation == bool:
                self.error(f'but has no response_collection_step:bool function argument')

        return 'COLLECTION'
