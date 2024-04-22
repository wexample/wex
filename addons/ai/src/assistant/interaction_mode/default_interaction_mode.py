from typing import List, Optional

from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import AbstractInteractionMode
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class DefaultInteractionMode(AbstractInteractionMode):
    @staticmethod
    def name() -> str:
        return "default"

    def process_user_input(
        self,
        prompt_section: UserPromptSection,
        remaining_sections: List[UserPromptSection]
    ) -> Optional[bool | str]:
        self.assistant.spinner.start()

        response = self.assistant.get_model().chat(
            prompt_section,
            self.get_interaction_mode_prompt_parameters(prompt_section)
        )

        self.assistant.spinner.stop()

        return response
