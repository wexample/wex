from typing import Optional, List, cast, TYPE_CHECKING, Dict

from chromadb import ClientAPI
from langchain_core.document_loaders import BaseLoader  # type: ignore
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from addons.ai.src.assistant.interaction_mode.abstract_vector_store_interaction_mode import AbstractVectorStoreInteractionMode

if TYPE_CHECKING:
    from ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject


class FileSearchInteractionMode(AbstractVectorStoreInteractionMode):
    chroma: Optional[ClientAPI] = None
    chroma_path: Optional[str] = None

    def __init__(self, subject: "AbstractChatSubject"):
        super().__init__(subject)
        self.init_vector_store()

    @staticmethod
    def name() -> str:
        return "file_search"

    def get_similarity_search_filter(self) -> Dict[str, str]:
        from addons.ai.src.assistant.subject.file_chat_subject import FileChatSubject
        subject = cast(FileChatSubject, self.assistant.get_current_subject())

        return {
            "source": subject.file_path
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

        self.vector_store_file(subject.file_path)

        # Avoid empty input error.
        if not prompt_section.prompt:
            return f'Please ask something about the file {subject.file_path}'

        self.assistant.spinner.start()

        response = self.assistant.get_model().chat(
            prompt_section,
            self.get_interaction_mode_prompt_parameters(prompt_section),
        )

        self.assistant.spinner.stop()

        return response
