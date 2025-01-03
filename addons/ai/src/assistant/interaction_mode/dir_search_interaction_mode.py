import os.path
from typing import TYPE_CHECKING, Dict, List, cast

import click
from langchain_core.document_loaders import BaseLoader  # type: ignore

from addons.ai.src.assistant.interaction_mode.abstract_vector_store_interaction_mode import (
    AbstractVectorStoreInteractionMode,
)
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import AbstractInteractionResponse
from addons.ai.src.assistant.interaction_response.string_interaction_response import StringInteractionResponse
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.const.globals import VERBOSITY_LEVEL_QUIET
from src.helper.file import file_build_signature, file_is_utf8_encoding

if TYPE_CHECKING:
    from addons.ai.src.assistant.subject.dir_chat_subject import DirChatSubject


class DirSearchInteractionMode(AbstractVectorStoreInteractionMode):
    def get_vector_store_collection_name(self) -> str:
        return "dir-search"

    def get_dir_subject(self) -> "DirChatSubject":
        return cast("DirChatSubject", self.assistant.get_current_subject())

    def get_storage_signature(self) -> str:
        return file_build_signature(self.get_dir_subject().dir_path)

    def get_similarity_search_filter(
        self, prompt_section: UserPromptSection
    ) -> Dict[str, str]:
        return {"signature": self.get_storage_signature()}

    def process_user_input(
        self,
        prompt_section: UserPromptSection,
        remaining_sections: List[UserPromptSection],
    ) -> AbstractInteractionResponse:
        subject = self.get_dir_subject()

        # Avoid empty input error.
        if not subject.dir_path:
            return StringInteractionResponse("No dir selected")

        if not os.path.exists(subject.dir_path):
            return StringInteractionResponse(f"Dir does not exists")

        storable_files = []

        for root, dirs, files in os.walk(subject.dir_path):
            for file in files:
                file_path = os.path.join(root, file)

                if file_is_utf8_encoding(file_path):
                    storable_files.append(file_path)
                else:
                    self.kernel.io.warn(
                        f"Non UTF-8 encoding detected on file {file_path}"
                    )

        verbosity = self.kernel.verbosity
        self.kernel.verbosity = VERBOSITY_LEVEL_QUIET
        with click.progressbar(storable_files) as bar:
            for file in bar:
                self.vector_store_file(file, file_build_signature(subject.dir_path))
        self.kernel.verbosity = verbosity
        self.last_stored_path = subject.dir_path

        # Avoid empty input error.
        if not prompt_section.prompt:
            return StringInteractionResponse(f"Please ask something about the directory {subject.dir_path}")

        return super().process_user_input(prompt_section, remaining_sections)
