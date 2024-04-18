from typing import List

from addons.ai.src.assistant.interaction_mode.default_interaction_mode import DefaultInteractionMode
from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject

ASSISTANT_INTERACTION_MODE_DEFAULT = "default"


class DefaultChatSubject(AbstractChatSubject):
    @staticmethod
    def name() -> str:
        return "default"

    def get_interaction_modes(self) -> List[type]:
        return [
            DefaultInteractionMode
        ]

    def is_fallback_subject(self) -> bool:
        return True
