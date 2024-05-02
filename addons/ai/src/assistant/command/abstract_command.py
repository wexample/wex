from abc import abstractmethod
from typing import Type, List, TYPE_CHECKING, Optional

from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import AbstractInteractionMode
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import AbstractInteractionResponse
from addons.ai.src.assistant.interaction_response.null_interaction_response import NullInteractionResponse
from addons.ai.src.assistant.utils.abstract_assistant_child import AbstractAssistantChild

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class AbstractCommand(AbstractAssistantChild):
    description: str = False
    sticky: bool = False
    root_only: str = False
    options: List[str] = []

    @staticmethod
    def name() -> str:
        pass

    def execute(
        self,
        prompt_section: Optional["UserPromptSection"] = None,
        remaining_sections: Optional[List["UserPromptSection"]] = None
    ) -> AbstractInteractionResponse:
        return NullInteractionResponse()

    @abstractmethod
    def get_interaction_mode(self, prompt_section: "UserPromptSection") -> Type[AbstractInteractionMode]:
        pass

    def is_active(self, current_prompt: str) -> bool:
        if self.root_only:
            return not self.assistant.text_has_a_command(current_prompt)
        return True
