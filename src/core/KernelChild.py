from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class KernelChild:
    kernel: "Kernel"

    def __init__(self, kernel: "Kernel") -> None:
        super().__init__()
        self.kernel = kernel

    def _validate__should_not_be_none(cls, value: Any) -> None:
        if value is None:
            raise ValueError("Property is not initialized")
        return value
