from typing import Optional, List

from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from addons.ai.src.assistant.utils.globals import AI_COMMAND_PREFIX
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.const.types import StringKeysDict
from src.helper.string import string_list_longest_word

SUBJECT_HELP_CHAT_COMMAND_HELP = "help"


class HelpChatSubject(AbstractChatSubject):
    @staticmethod
    def name() -> str:
        return "help"

    def introduce(self) -> str:
        return f"Display help"

    def get_completer_commands(self) -> StringKeysDict:
        return {
            SUBJECT_HELP_CHAT_COMMAND_HELP: "Show help",
        }

    def process_prompt_section(
        self,
        prompt_section: UserPromptSection,
        remaining_sections: List[UserPromptSection]
    ) -> Optional[bool | str]:
        self.show_help()
        return True

    def show_help(self) -> None:
        commands = self.assistant.get_active_commands()
        # Assuming string_list_longest_word returns the length of the longest word in a list
        longest_command_length = string_list_longest_word(commands.keys())

        # Display the menu in the specified format
        for command, description in commands.items():
            # Pad the command with spaces to align all descriptions
            padded_command = command.ljust(longest_command_length)
            self.assistant.log(f"{AI_COMMAND_PREFIX}{padded_command} | {description}")

        self.assistant.log(f"Press Alt+Enter to add a new line")
