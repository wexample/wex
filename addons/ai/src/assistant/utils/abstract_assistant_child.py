from typing import TYPE_CHECKING

from src.utils.abstract_kernel_child import AbsractKernelChild

if TYPE_CHECKING:
    from addons.ai.src.assistant.assistant import Assistant


class AbstractAssistantChild(AbsractKernelChild):
    def __init__(self, assistant: "Assistant") -> None:
        super().__init__(assistant.kernel)

        self.assistant = assistant
