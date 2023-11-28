from typing import TYPE_CHECKING

from src.core.BaseClass import BaseClass

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class KernelChild(BaseClass):
    kernel: "Kernel"

    def __init__(self, kernel: "Kernel") -> None:
        super().__init__()
        self.kernel = kernel
