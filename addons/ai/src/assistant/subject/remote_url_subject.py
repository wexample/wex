from typing import List

from addons.ai.src.assistant.interaction_mode.url_search_interaction_mode import UrlSearchInteractionMode
from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from src.const.types import StringKeysDict

SUBJECT_PREVIOUS_RESPONSE_COMMAND_FETCH_URL = "fetch_url"


class RemoteUrlSubject(AbstractChatSubject):
    @staticmethod
    def name() -> str:
        return "remote_url"

    def introduce(self) -> str:
        return f"Talk about a remote website"

    def get_interaction_modes(self) -> List[type]:
        return [
            UrlSearchInteractionMode,
        ]

    def get_commands(self) -> StringKeysDict:
        return {
            SUBJECT_PREVIOUS_RESPONSE_COMMAND_FETCH_URL: "Fetch web page content from URL"
        }
