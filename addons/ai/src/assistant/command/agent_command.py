from typing import TYPE_CHECKING, Type

from addons.ai.src.assistant.command.default_command import DefaultCommand
from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import \
    AbstractInteractionMode
from addons.ai.src.assistant.interaction_mode.tool_picker_interaction_mode import \
    ToolPickerInteractionMode

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import \
        UserPromptSection


class AgentCommand(DefaultCommand):
    description: str = "Ask agent to use a tool (beta)"

    @staticmethod
    def name() -> str:
        return "agent"

    def get_interaction_mode(
        self, prompt_section: "UserPromptSection"
    ) -> Type[AbstractInteractionMode]:
        return ToolPickerInteractionMode
