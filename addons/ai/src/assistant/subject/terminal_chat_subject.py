import os
from typing import Optional, List

from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.const.types import StringKeysDict
from src.helper.command import execute_command_sync

SUBJECT_FILE_CHAT_COMMAND_TERMINAL = "terminal"


class TerminalChatSubject(AbstractChatSubject):
    dir_path: Optional[str] = None

    @staticmethod
    def name() -> str:
        return "terminal"

    def introduce(self) -> str:
        return f"Dealing with cli terminal"

    def get_commands(self) -> StringKeysDict:
        return {
            SUBJECT_FILE_CHAT_COMMAND_TERMINAL: "Execute a command in the terminal",
        }

    def process_prompt_section(
        self,
        prompt_section: UserPromptSection,
        remaining_sections: List[UserPromptSection]
    ) -> Optional[bool | str]:
        success, response = execute_command_sync(
            self.kernel,
            prompt_section.prompt,
            ignore_error=True,
            shell=True
        )

        response_str = os.linesep.join(response)
        self.assistant.get_current_session_history().add_message(response_str)

        return ("Running: "
                + prompt_section.prompt
                + ":" + os.linesep
                + response_str)
