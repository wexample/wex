from typing import TYPE_CHECKING

from src.utils.abstract_kernel_child import AbsractKernelChild

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


class AddonManager(AbsractKernelChild):
    def __init__(self, kernel: "Kernel", name: str) -> None:
        super().__init__(kernel)

        self.name: str = name
