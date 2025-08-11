from typing import TYPE_CHECKING, Optional, List

from addons.ai.src.assistant.command.abstract_command import AbstractCommand
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import AbstractInteractionResponse
from addons.ai.src.assistant.utils.globals import AI_COMMAND_PREFIX
from src.helper.string import string_list_longest_word

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class HelpCommand(AbstractCommand):
    description: str = "Show help"

    @staticmethod
    def name() -> str:
        return "help"

    def execute(
        self,
        prompt_section: Optional["UserPromptSection"] = None,
        remaining_sections: Optional[List["UserPromptSection"]] = None
    ) -> AbstractInteractionResponse:
        commands = self.assistant.get_active_commands()
        # Assuming string_list_longest_word returns the length of the longest word in a list
        longest_command_length = string_list_longest_word(list(commands.keys()))

        # Display the menu in the specified format
        for command_name, command in commands.items():
            # Pad the command with spaces to align all descriptions
            padded_command = command_name.ljust(longest_command_length)
            self.assistant.log(
                f"{AI_COMMAND_PREFIX}{padded_command} | {command.description}"
            )

            for option in command.get_flags():
                self.assistant.log(
                    f"    :{option}"
                )

        self.assistant.log(f"Press Alt+Enter to add a new line")

        return super().execute(prompt_section, remaining_sections)
