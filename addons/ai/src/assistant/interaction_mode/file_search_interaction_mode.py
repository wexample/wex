from typing import Dict, List, cast, TYPE_CHECKING

from langchain_core.document_loaders import BaseLoader  # type: ignore

from addons.ai.src.assistant.interaction_mode.abstract_vector_store_interaction_mode import (
    AbstractVectorStoreInteractionMode,
)
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import AbstractInteractionResponse
from addons.ai.src.assistant.interaction_response.string_interaction_response import StringInteractionResponse
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.helper.file import file_build_signature

if TYPE_CHECKING:
    from addons.ai.src.assistant.subject.file_chat_subject import FileChatSubject


class FileSearchInteractionMode(AbstractVectorStoreInteractionMode):
    def get_vector_store_collection_name(self) -> str:
        return "file-search"

    def get_file_subject(self) -> "FileChatSubject":
        return cast("FileChatSubject", self.assistant.get_current_subject())

    def get_storage_signature(self) -> str:
        return file_build_signature(self.get_file_subject().file_path)

    def get_similarity_search_filter(
        self, prompt_section: UserPromptSection
    ) -> Dict[str, str]:
        return {"signature": self.get_storage_signature()}

    def process_user_input(
        self,
        prompt_section: UserPromptSection,
        remaining_sections: List[UserPromptSection],
    ) -> AbstractInteractionResponse:
        from addons.ai.src.assistant.subject.file_chat_subject import FileChatSubject

        subject = cast(FileChatSubject, self.assistant.get_current_subject())

        # Avoid empty input error.
        if not subject.file_path:
            return StringInteractionResponse(f"No file selected")

        self.vector_store_file(
            subject.file_path,
            self.get_storage_signature()
        )

        # Avoid empty input error.
        if not prompt_section.prompt:
            return StringInteractionResponse(f"Please ask something about the file {subject.file_path}")

        return super().process_user_input(prompt_section, remaining_sections)
