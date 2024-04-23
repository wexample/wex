from abc import abstractmethod
from typing import List, cast, Dict, Optional

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

    def get_completer_commands(self) -> StringKeysDict:
        return {}

    def introduce(self) -> str:
        return self.name()

    def get_interaction_mode(self, prompt_section: Optional[UserPromptSection] = None) -> Optional[type]:
        modes = self.get_interaction_modes()
        if not len(modes):
            return None

        assert len(modes)

        first_mode = modes[0]
        assert issubclass(first_mode, AbstractInteractionMode)
        return first_mode

    @abstractmethod
    def get_interaction_modes(self) -> List[type]:
        return []

    def is_current_subject(self) -> bool:
        return self.assistant.get_current_subject() == self

    def use_as_current_subject(self, prompt_section: UserPromptSection) -> bool:
        if not self.is_current_subject():
            # But command match with allowed ones, or this is a fallback.
            if (
                prompt_section.command and
                prompt_section.command in self.get_completer_commands()
            ) or self.is_fallback_subject():
                # So this is the new subject.
                self.assistant.set_subject(self.name(), prompt_section)
            else:
                return False
        return True

    def is_fallback_subject(self) -> bool:
        """
        Ask to execute subject, even no command explicitly prompted by the user.
        :return:
        """
        return False

    def activate(self, prompt_section: Optional[UserPromptSection] = None) -> bool:
        # Build interaction modes classes
        interaction_modes: Dict[str, AbstractInteractionMode] = {}
        for interaction_mode_class in self.get_interaction_modes():
            instance = cast(AbstractInteractionMode, interaction_mode_class(self))
            interaction_modes[instance.name()] = instance

        self.interaction_modes = interaction_modes

        return True

    def get_prompt_parameters(self) -> Dict:
        return {}

    def process_prompt_section(
        self,
        prompt_section: UserPromptSection,
        remaining_sections: List[UserPromptSection]
    ) -> Optional[bool | str]:
        # Set default
        mode = self.get_interaction_mode(prompt_section)
        interaction_mode = self.interaction_modes[cast(AbstractInteractionMode, mode).name()] if mode else None

        # By default interaction mode is required.
        if not interaction_mode:
            self.assistant.log(f"No interaction mode defined for subject : {self.name()}")
            return False

        return interaction_mode.process_user_input(
            prompt_section,
            remaining_sections
        )
