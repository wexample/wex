from typing import Optional

from addons.ai.src.assistant.utils.abstract_assistant_child import AbstractAssistantChild
from src.const.types import StringKeysDict


class AbstractChatSubject(AbstractAssistantChild):
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
