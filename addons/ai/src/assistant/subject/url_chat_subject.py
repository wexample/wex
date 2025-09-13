from __future__ import annotations


import validators

from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class UrlChatSubject(AbstractChatSubject):
    url: str | None = None

    @staticmethod
    def name() -> str:
        return "url"

    def introduce(self) -> str:
        return f"Chatting about URL {self.url}"

    def activate(self, prompt_section: UserPromptSection | None = None) -> bool:
        if super().activate():
            user_input = prompt_section.prompt if prompt_section else None
            user_input_trimmed = user_input.strip() if user_input else None

            if not user_input_trimmed:
                self.assistant.log(f"Please provide a URL")
                return False

            if not validators.url(user_input_trimmed):
                self.assistant.log(f"Provided URL is not valid: {user_input_trimmed}")
                return False

            self.url = user_input_trimmed
            return True

        return False
