from typing import List

from addons.ai.src.assistant.interaction_mode.function_picker_interaction_mode import FunctionPickerInteractionMode
from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from src.const.types import StringKeysDict

SUBJECT_FUNCTION_CHAT_COMMAND_AGENT = "function"


class FunctionChatSubject(AbstractChatSubject):
    @staticmethod
    def name() -> str:
        return "function"

    def introduce(self) -> str:
        return f"Execute a function selected by tagging system (beta)"

    def get_completer_commands(self) -> StringKeysDict:
        return {
            SUBJECT_FUNCTION_CHAT_COMMAND_AGENT: "Use a function (beta)",
        }

    def get_interaction_modes(self) -> List[type]:
        return [
            FunctionPickerInteractionMode
        ]

