from typing import Optional, List

from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from addons.ai.src.assistant.utils.globals import AI_FUNCTION_DISPLAY_A_CUCUMBER, AI_IDENTITY_COMMAND_SELECTOR
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.const.types import StringKeysDict

SUBJECT_FUNCTION_CHAT_COMMAND_AGENT = "function"


class FunctionChatSubject(AbstractChatSubject):
    @staticmethod
    def name() -> str:
        return "function"

    def introduce(self) -> str:
        return f"Execute a function selected by tagging system (beta)"

    def get_completer_commands(self) -> StringKeysDict:
        return {
            SUBJECT_FUNCTION_CHAT_COMMAND_AGENT: "Use a function (beta)",
        }

    def process_user_input(
        self,
        prompt_section: UserPromptSection,
        identity: StringKeysDict,
        identity_parameters: StringKeysDict,
        remaining_sections: List[UserPromptSection]
    ) -> Optional[bool | str]:
        if not prompt_section.prompt:
            return "Please ask some question to help select a function."

        selected_function = self.assistant.get_model().guess_function(
            prompt_section.prompt,
            [
                AI_FUNCTION_DISPLAY_A_CUCUMBER,
                None,
            ],
            self.assistant.identities[AI_IDENTITY_COMMAND_SELECTOR],
        )

        # Demo usage
        if selected_function == AI_FUNCTION_DISPLAY_A_CUCUMBER:
            return "🥒"
        else:
            self.assistant.log(f"No function selected : {str(selected_function)}")

        return True
