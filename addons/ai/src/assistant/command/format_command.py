from typing import TYPE_CHECKING, List, Type

from addons.ai.src.assistant.command.default_command import DefaultCommand
from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import \
    AbstractInteractionMode
from addons.ai.src.assistant.interaction_mode.formated_data_interaction_mode import (
    FORMATED_DATA_FORMATS, FormatedDataInteractionMode)

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import \
        UserPromptSection


class FormatCommand(DefaultCommand):
    description: str = "Return formated response"

    @staticmethod
    def name() -> str:
        return "format"

    def get_flags(self) -> List[str]:
        return FORMATED_DATA_FORMATS

    def get_interaction_mode(
        self, prompt_section: "UserPromptSection"
    ) -> Type[AbstractInteractionMode]:
        return FormatedDataInteractionMode
