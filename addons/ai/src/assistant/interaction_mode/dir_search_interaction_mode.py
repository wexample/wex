import os.path
from typing import Optional, TYPE_CHECKING, List, cast, Dict

from langchain_core.document_loaders import BaseLoader  # type: ignore

from addons.ai.src.assistant.interaction_mode.abstract_vector_store_interaction_mode import \
    AbstractVectorStoreInteractionMode
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.helper.file import file_is_utf8_encoding

if TYPE_CHECKING:
    from ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject


class DirSearchInteractionMode(AbstractVectorStoreInteractionMode):
    def __init__(self, subject: "AbstractChatSubject"):
        super().__init__(subject)
        self.init_vector_store()

    @staticmethod
    def name() -> str:
        return "dir_search"

    def get_similarity_search_filter(self) -> Dict[str, str]:
        from addons.ai.src.assistant.subject.dir_chat_subject import DirChatSubject
        subject = cast(DirChatSubject, self.assistant.get_current_subject())

        return {
            "source": subject.dir_path
        }

    def process_user_input(
        self,
        prompt_section: UserPromptSection,
        remaining_sections: List[UserPromptSection]
    ) -> Optional[bool | str]:
        from addons.ai.src.assistant.subject.dir_chat_subject import DirChatSubject
        subject = cast(DirChatSubject, self.assistant.get_current_subject())

        # Avoid empty input error.
        if not subject.dir_path:
            return f'No dir selected'

        if not os.path.exists(subject.dir_path):
            return f'Dir does not exists'

        for root, dirs, files in os.walk(subject.dir_path):
            for file in files:
                file_path = os.path.join(root, file)

                if file_is_utf8_encoding(file_path):
                    self.vector_store_file(file_path)
                else:
                    self.kernel.io.warn(f"Non UTF-8 encoding detected on file {file_path}")

        # Avoid empty input error.
        if not prompt_section.prompt:
            return f'Please ask something about the directory {subject.dir_path}'

        self.assistant.spinner.start()

        response = self.assistant.get_model().chat(
            prompt_section,
            self.get_interaction_mode_prompt_parameters(prompt_section),
        )

        self.assistant.spinner.stop()

        return response
