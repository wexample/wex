from abc import abstractmethod
from typing import Type, List, TYPE_CHECKING

from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import AbstractInteractionMode
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import AbstractInteractionResponse
from addons.ai.src.assistant.interaction_response.null_interaction_response import NullInteractionResponse

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class AbstractCommand(object):
    def __init__(self):
        self.options: List[str] = []

    @staticmethod
    def name() -> str:
        pass

    def execute(self, prompt_section: "UserPromptSection") -> AbstractInteractionResponse:
        return NullInteractionResponse()

    @abstractmethod
    def get_interaction_mode(self, prompt_section: "UserPromptSection") -> Type[AbstractInteractionMode]:
        pass
