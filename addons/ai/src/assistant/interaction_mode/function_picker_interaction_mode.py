from typing import List, Optional

from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import (
    AbstractInteractionMode,
)
from addons.ai.src.assistant.utils.globals import AI_FUNCTION_DISPLAY_A_CUCUMBER
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class FunctionPickerInteractionMode(AbstractInteractionMode):
    @staticmethod
    def name() -> str:
        return "function_picker"

    def get_initial_prompt(self, prompt_section: UserPromptSection) -> Optional[str]:
        return "Provide a command name that aids in responding to the user's query, or None if not applicable."

    def process_user_input(
        self,
        prompt_section: UserPromptSection,
        remaining_sections: List[UserPromptSection],
    ) -> Optional[bool | str]:
        if not prompt_section.prompt:
            return "Please ask some question to help select a function."

        selected_function = self.assistant.get_model().guess_function(
            self,
            prompt_section,
            [
                AI_FUNCTION_DISPLAY_A_CUCUMBER,
                None,
            ],
        )

        # Demo usage
        if selected_function == AI_FUNCTION_DISPLAY_A_CUCUMBER:
            return "🥒"
        else:
            self.assistant.log(f"No function selected : {str(selected_function)}")

        return True
