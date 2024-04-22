import os.path
from typing import Optional, TYPE_CHECKING, List, cast, Dict

import click
from langchain_core.document_loaders import BaseLoader  # type: ignore

from addons.ai.src.assistant.interaction_mode.abstract_vector_store_interaction_mode import \
    AbstractVectorStoreInteractionMode
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.const.globals import VERBOSITY_LEVEL_QUIET
from src.helper.file import file_is_utf8_encoding, file_build_signature

if TYPE_CHECKING:
    from ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject


class DirSearchInteractionMode(AbstractVectorStoreInteractionMode):
    def __init__(self, subject: "AbstractChatSubject"):
        super().__init__(subject)
        # Use a temporary trick to not vectorize any file
        self.last_stored_path: Optional[str] = None

    @staticmethod
    def name() -> str:
        return "dir_search"

    def get_similarity_search_filter(self, prompt_section: UserPromptSection) -> Dict[str, str]:
        from addons.ai.src.assistant.subject.dir_chat_subject import DirChatSubject
        subject = cast(DirChatSubject, self.assistant.get_current_subject())

        return {
            "signature": self.last_stored_path
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

        if self.last_stored_path != subject.dir_path:
            storable_files = []

            for root, dirs, files in os.walk(subject.dir_path):
                for file in files:
                    file_path = os.path.join(root, file)

                    if file_is_utf8_encoding(file_path):
                        storable_files.append(file_path)
                    else:
                        self.kernel.io.warn(f"Non UTF-8 encoding detected on file {file_path}")

            verbosity = self.kernel.verbosity
            self.kernel.verbosity = VERBOSITY_LEVEL_QUIET
            with click.progressbar(storable_files) as bar:
                for file in bar:
                    self.vector_store_file(file, file_build_signature(subject.dir_path))
            self.kernel.verbosity = verbosity
            self.last_stored_path = subject.dir_path

        # Avoid empty input error.
        if not prompt_section.prompt:
            return f'Please ask something about the directory {subject.dir_path}'

        return super().process_user_input(
            prompt_section,
            remaining_sections
        )
