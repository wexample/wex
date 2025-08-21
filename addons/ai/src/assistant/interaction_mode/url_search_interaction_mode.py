from typing import TYPE_CHECKING, Dict, List, cast

from addons.ai.src.assistant.interaction_mode.abstract_vector_store_interaction_mode import \
    AbstractVectorStoreInteractionMode
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import \
    AbstractInteractionResponse
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection

if TYPE_CHECKING:
    from addons.ai.src.assistant.subject.url_chat_subject import UrlChatSubject


class UrlSearchInteractionMode(AbstractVectorStoreInteractionMode):
    def get_vector_store_collection_name(self) -> str:
        return "url-search"

    def get_storage_signature(self) -> str:
        return self.get_url()

    def get_similarity_search_filter(
        self, prompt_section: UserPromptSection
    ) -> Dict[str, str]:
        return {"signature": self.get_url()}

    def get_url_subject(self) -> "UrlChatSubject":
        return cast("UrlChatSubject", self.assistant.get_current_subject())

    def get_url(self) -> str:
        return self.get_url_subject().url or ""

    def process_user_input(
        self,
        prompt_section: UserPromptSection,
        remaining_sections: List[UserPromptSection],
    ) -> AbstractInteractionResponse:
        self.vector_store_url(self.get_url(), self.get_storage_signature())

        return super().process_user_input(prompt_section, remaining_sections)
