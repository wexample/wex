from abc import abstractmethod
from src.const.globals import KERNEL_RENDER_MODE_CLI


class AbstractResponse:
    def __init__(self, kernel):
        from src.core.Kernel import Kernel
        self.request = kernel.current_request
        self.kernel: Kernel = kernel
        self.parent = None

    def get_root_parent(self):
        if self.parent:
            return self.parent.get_root_parent()
        return self

    @abstractmethod
    def render(self, render_mode: str = KERNEL_RENDER_MODE_CLI, args: dict = None) -> str | int | bool | None:
        pass
