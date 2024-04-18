from typing import List

from addons.ai.src.assistant.interaction_mode.tool_picker_interaction_mode import ToolPickerInteractionMode
from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from src.const.types import StringKeysDict

SUBJECT_TOOL_CHAT_COMMAND_AGENT = "agent"


class AgentChatSubject(AbstractChatSubject):
    @staticmethod
    def name() -> str:
        return "agent"

    def get_interaction_modes(self) -> List[type]:
        return [
            ToolPickerInteractionMode
        ]

    def introduce(self) -> str:
        return f"Ask agent to use a tool (beta)"

    def get_completer_commands(self) -> StringKeysDict:
        return {
            SUBJECT_TOOL_CHAT_COMMAND_AGENT: "Ask agent to use a tool",
        }
