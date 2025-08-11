from typing import TYPE_CHECKING, Type

from addons.ai.src.assistant.command.default_command import DefaultCommand
from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import AbstractInteractionMode
from addons.ai.src.assistant.interaction_mode.url_search_interaction_mode import UrlSearchInteractionMode
from addons.ai.src.assistant.subject.url_chat_subject import UrlChatSubject

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class UrlSearchCommand(DefaultCommand):
    description: str = "Similarity search into web page"
    root_only: bool = True

    @staticmethod
    def name() -> str:
        return "url-search"

    def is_active(self, current_prompt: str) -> bool:
        return isinstance(self.assistant.subject, UrlChatSubject)

    def get_interaction_mode(self, prompt_section: "UserPromptSection") -> Type[AbstractInteractionMode]:
        return UrlSearchInteractionMode
