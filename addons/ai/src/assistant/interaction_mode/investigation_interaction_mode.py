from typing import Optional

from addons.ai.src.assistant.interaction_mode.default_interaction_mode import (
    DefaultInteractionMode,
)
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class InvestigationInteractionMode(DefaultInteractionMode):
    def get_initial_prompt(self, prompt_section: UserPromptSection) -> Optional[str]:
        return (
            "You will ask the user questions so that we can identify the source of the problem together."
            "Start with only the first question. "
            "Save as much text as possible so that the discussion can be reread quickly, "
            "no unnecessary introductions or explanations. "
            "The user will provide what they find, "
            "Never use any kind of ordered or unordered lists. "
            "and then you will ask the next question based on that result."
        )
