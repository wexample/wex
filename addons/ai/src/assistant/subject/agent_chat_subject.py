from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from src.const.types import StringKeysDict

SUBJECT_AGENT_COMMAND_AGENT = "agent"


class AgentChatSubject(AbstractChatSubject):
    @staticmethod
    def name() -> str:
        return "agent"

    def introduce(self) -> str:
        return f"Ask agent to use a tool (beta)"

    def get_commands(self) -> StringKeysDict:
        return {
            SUBJECT_AGENT_COMMAND_AGENT: "Ask agent to use a tool",
        }
