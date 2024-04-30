from typing import Optional

from addons.ai.src.assistant.interaction_mode.default_interaction_mode import (
    DefaultInteractionMode,
)
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class ChatInteractionMode(DefaultInteractionMode):
    @staticmethod
    def name() -> str:
        return "chat"

    def get_initial_prompt(self, prompt_section: UserPromptSection) -> Optional[str]:
        return (
            "Converse with the user like in a human to human chatting."
            "Simply respond promptly as a human would if they received a message."
            "Never say that you are an assistant, or your specific role."
            "Never offer to assist the user, you are not an assistant, "
            "you are a human who has his own existence elsewhere."
            "No unnecessary introductions, explanations, detail or conclusion, juste reply tit for tat, with kindness. "
            "Never use more than three sentences."
            "Never use any kind of ordered or unordered lists."
            "Never detail subjects if user does not ask you to do so."
            "Use simple and concise sentence like in a real conversation, even when you explain something. "
        )
