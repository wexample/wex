from typing import Type, TYPE_CHECKING

from addons.ai.src.assistant.command.default_command import DefaultCommand
from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import AbstractInteractionMode
from addons.ai.src.assistant.interaction_mode.function_picker_interaction_mode import FunctionPickerInteractionMode

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class FunctionCommand(DefaultCommand):
    description: str = "Execute a function selected by tagging system (beta)"

    @staticmethod
    def name() -> str:
        return "function"

    def get_interaction_mode(self, prompt_section: "UserPromptSection") -> Type[AbstractInteractionMode]:
        return FunctionPickerInteractionMode
