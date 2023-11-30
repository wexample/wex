from typing import TYPE_CHECKING

from src.core.KernelChild import KernelChild

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class AddonManager(KernelChild):
    def __init__(self, kernel: "Kernel", name: str) -> None:
        super().__init__(kernel)
        
        self.name: str = name
