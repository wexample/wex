from abc import abstractmethod
from src.const.globals import KERNEL_RENDER_MODE_CLI


class AbstractResponse:
    def __init__(self, kernel):
        from src.core.Kernel import Kernel
        self.request = kernel.current_request
        self.kernel: Kernel = kernel

    @abstractmethod
    def render(self, render_mode: str = KERNEL_RENDER_MODE_CLI) -> str | int | bool | None:
        pass
