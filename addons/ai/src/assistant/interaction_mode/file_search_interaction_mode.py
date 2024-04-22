from typing import Optional, List, cast, Dict

from langchain_core.document_loaders import BaseLoader  # type: ignore

from addons.ai.src.assistant.interaction_mode.abstract_vector_store_interaction_mode import \
    AbstractVectorStoreInteractionMode
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.helper.file import file_build_signature


class FileSearchInteractionMode(AbstractVectorStoreInteractionMode):
    @staticmethod
    def name() -> str:
        return "file_search"

    def get_similarity_search_filter(self, prompt_section: UserPromptSection) -> Dict[str, str]:
        from addons.ai.src.assistant.subject.file_chat_subject import FileChatSubject
        subject = cast(FileChatSubject, self.assistant.get_current_subject())

        return {
            "signature": file_build_signature(subject.file_path)
        }

    def process_user_input(
        self,
        prompt_section: UserPromptSection,
        remaining_sections: List[UserPromptSection]
    ) -> Optional[bool | str]:
        from addons.ai.src.assistant.subject.file_chat_subject import FileChatSubject
        subject = cast(FileChatSubject, self.assistant.get_current_subject())

        # Avoid empty input error.
        if not subject.file_path:
            return f'No file selected'

        self.vector_store_file(subject.file_path, file_build_signature(subject.file_path))

        # Avoid empty input error.
        if not prompt_section.prompt:
            return f'Please ask something about the file {subject.file_path}'

        return super().process_user_input(
            prompt_section,
            remaining_sections
        )
