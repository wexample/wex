from src.const.globals import KERNEL_RENDER_MODE_CLI
from src.core.response.AbstractResponse import AbstractResponse


class ResponseCollectionResponse(AbstractResponse):
    def __init__(self, kernel, collection: list):
        super().__init__(kernel)

        self.collection = collection

    def render(self, render_mode: str = KERNEL_RENDER_MODE_CLI) -> str | int | bool | None:
        return 'COLLECTION'
