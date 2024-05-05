import os
from typing import Optional, List, cast

from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import (
    AbstractInteractionMode,
)
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import AbstractInteractionResponse
from addons.ai.src.assistant.interaction_response.string_interaction_response import StringInteractionResponse
from addons.ai.src.assistant.subject.file_chat_subject import FileChatSubject
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.helper.file import file_read, file_write


class FileRewriteInteractionMode(AbstractInteractionMode):
    file_length_limit: int = 1000

    def get_initial_prompt(self, prompt_section: UserPromptSection) -> Optional[str]:
        return (
            f"You will give a new version of this file, following given guidelines. "
            f"Return the whole new file content with any other text before or after. "
            f"Include unchanged parts of the original file if still present in the new version. "
            "No introduction. No conclusion. No markdown code block."
        )

    def process_user_input(
        self,
        prompt_section: "UserPromptSection",
        remaining_sections: List["UserPromptSection"],
    ) -> AbstractInteractionResponse:
        if not prompt_section.prompt:
            return StringInteractionResponse("Please provide a guideline to indicate what to change in the file")

        subject = cast(FileChatSubject, self.assistant.subject)
        file_content = file_read(subject.file_path)

        if len(file_content) > self.file_length_limit:
            return StringInteractionResponse(
                f"The file content should not exceed {self.file_length_limit} characters,"
                f" got {len(file_content)}")

        prompt_section.prompt_configurations += [
            ("system", "##FILE CONTENT" + os.linesep + file_content)
        ]

        response = super().process_user_input(
            prompt_section,
            remaining_sections,
        )

        file_write(subject.file_path, response.render())

        self.assistant.log("File has been rewritten")

        return response
