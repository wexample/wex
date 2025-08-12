from typing import TYPE_CHECKING

from src.core.BaseClass import BaseClass

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


class AbsractKernelChild(BaseClass):
    kernel: "Kernel"

    def __init__(self, kernel: "Kernel") -> None:
        super().__init__()
        self.kernel = kernel
