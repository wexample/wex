from abc import abstractmethod

from src.const.globals import KERNEL_RENDER_MODE_CLI


class AbstractResponse:
    @abstractmethod
    def render(self, kernel, render_mode: str = KERNEL_RENDER_MODE_CLI) -> str:
        pass
