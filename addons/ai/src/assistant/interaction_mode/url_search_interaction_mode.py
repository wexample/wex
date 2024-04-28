from typing import TYPE_CHECKING, Dict, List, Optional

import validators

from addons.ai.src.assistant.interaction_mode.abstract_vector_store_interaction_mode import (
    AbstractVectorStoreInteractionMode,
)
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection

if TYPE_CHECKING:
    from ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject


class UrlSearchInteractionMode(AbstractVectorStoreInteractionMode):
    def __init__(self, subject: "AbstractChatSubject") -> None:
        super().__init__(subject)
        # Use a temporary trick to not vectorize any file
        self.last_stored_url: Optional[str] = None

    @staticmethod
    def name() -> str:
        return "url_search"

    def get_similarity_search_filter(
        self, prompt_section: UserPromptSection
    ) -> Dict[str, str]:
        return {"signature": self.last_stored_url}

    def process_user_input(
        self,
        prompt_section: UserPromptSection,
        remaining_sections: List[UserPromptSection],
    ) -> Optional[bool | str]:
        if not self.last_stored_url:
            if not prompt_section.prompt:
                return f"Please provide a URL"

            if not validators.url(prompt_section.prompt):
                return f"Provided URL is not valid: {prompt_section.prompt}"

            self.vector_store_url(prompt_section.prompt, prompt_section.prompt)
            self.last_stored_url = prompt_section.prompt

            return f"Please ask something about the URL {self.last_stored_url}"

        return super().process_user_input(prompt_section, remaining_sections)
