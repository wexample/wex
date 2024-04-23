from abc import abstractmethod
from typing import List, Dict, Optional

from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import AbstractInteractionMode
from addons.ai.src.assistant.utils.abstract_assistant_child import AbstractAssistantChild
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.const.types import StringKeysDict


class AbstractChatSubject(AbstractAssistantChild):
    interaction_modes: Dict[str, AbstractInteractionMode]
    interaction_mode: Optional[AbstractInteractionMode]

    @staticmethod
    def name() -> str:
        pass

    def get_commands(self) -> StringKeysDict:
        return {}

    def introduce(self) -> str:
        return self.name()

    @abstractmethod
    def get_interaction_mode(self, prompt_section: Optional[UserPromptSection] = None) -> Optional[type]:
        pass

    def is_current_subject(self) -> bool:
        return self.assistant.get_current_subject() == self

    def use_as_current_subject(self, prompt_section: UserPromptSection) -> bool:
        if not self.is_current_subject():
            # But command match with allowed ones, or this is a fallback.
            if (
                prompt_section.command and
                prompt_section.command in self.get_commands()
            ) or self.is_fallback_subject():
                # So this is the new subject.
                self.assistant.set_subject(self.name())
            else:
                return False
        return True

    def is_fallback_subject(self) -> bool:
        """
        Ask to execute subject, even no command explicitly prompted by the user.
        :return:
        """
        return False

    def get_prompt_parameters(self) -> Dict:
        return {}

    def process_prompt_section(
        self,
        prompt_section: UserPromptSection,
        remaining_sections: List[UserPromptSection]
    ) -> Optional[bool | str]:
        # Set default
        mode = self.get_interaction_mode(prompt_section)
        interaction_mode: AbstractInteractionMode = mode(self)

        # By default interaction mode is required.
        if not interaction_mode:
            self.assistant.log(f"No interaction mode defined for subject : {self.name()}")
            return False

        return interaction_mode.process_user_input(
            prompt_section,
            remaining_sections
        )
