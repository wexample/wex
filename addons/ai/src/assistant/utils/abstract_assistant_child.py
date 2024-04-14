from typing import TYPE_CHECKING

from src.core.KernelChild import KernelChild

if TYPE_CHECKING:
    from addons.ai.src.assistant.assistant import Assistant


class AbstractAssistantChild(KernelChild):
    def __init__(self, assistant: "Assistant") -> None:
        super().__init__(assistant.kernel)

        self.assistant = assistant
