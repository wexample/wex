from typing import TYPE_CHECKING, Optional

from src.const.types import StringKeysDict, StringsList
from src.core.KernelChild import KernelChild

if TYPE_CHECKING:
    from addons.ai.src.assistant.assistant import Assistant


class AbstractChatSubject(KernelChild):
    def __init__(self, assistant: "Assistant") -> None:
        super().__init__(assistant.kernel)

        self.assistant = assistant

    @staticmethod
    def name() -> str:
        pass

    def get_completer_commands(self) -> StringKeysDict:
        return {}

    def introduce(self) -> str:
        return self.name()

    def process_user_input(
        self,
        user_input_split: StringKeysDict,
        identity: StringKeysDict,
        identity_parameters: StringKeysDict,
    ) -> Optional[str]:
        return None

    def is_current_subject(self) -> bool:
        return self.assistant.get_current_subject() == self
