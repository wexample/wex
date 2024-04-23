from typing import Optional

from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import AbstractInteractionMode
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class VettingInteractionMode(AbstractInteractionMode):

    def get_initial_prompt(self, prompt_section: UserPromptSection) -> Optional[str]:
        return "Provide a command name that aids in responding to the user's query, or None if not applicable."
