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
            "No unnecessary introductions or explanations. "
            "Use simple and concise sentence like in a real conversation, even when you explain something. "
        )
