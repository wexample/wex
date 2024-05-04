from typing import TYPE_CHECKING, Type

from addons.ai.src.assistant.command.default_command import DefaultCommand
from addons.ai.src.assistant.interaction_mode.vetting_interaction_mode import VettingInteractionMode

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class VetCommand(DefaultCommand):
    description: str = "Vet a people based on given data"

    @staticmethod
    def name() -> str:
        return "vet"

    def get_interaction_mode(self, prompt_section: "UserPromptSection") -> Type[VettingInteractionMode]:
        return VettingInteractionMode
