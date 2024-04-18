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

    @abstractmethod
    def get_default_interaction_mode(self) -> Optional[str]:
        modes = self.get_interaction_modes()
        if not len(modes):
            return None

        assert len(modes)

        first_mode = modes[0]
        assert issubclass(first_mode, AbstractInteractionMode)
        return first_mode.name()

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

    @abstractmethod
    def activate(self, prompt_section: Optional[UserPromptSection] = None) -> bool:
        # Build interaction modes classes
        interaction_modes: Dict[str, AbstractInteractionMode] = {}
        for interaction_mode_class in self.get_interaction_modes():
            instance = cast(AbstractInteractionMode, interaction_mode_class(self))
            interaction_modes[instance.name()] = instance

        self.interaction_modes = interaction_modes

        # Set default
        mode_name = self.get_default_interaction_mode()
        self.interaction_mode = interaction_modes[mode_name] if mode_name else None

        return True

    def get_prompt_parameters(self) -> Dict:
        return {}
