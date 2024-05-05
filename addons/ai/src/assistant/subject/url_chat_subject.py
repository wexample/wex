from typing import Optional

import validators

from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class UrlChatSubject(AbstractChatSubject):
    url: Optional[str] = None

    @staticmethod
    def name() -> str:
        return "file"

    def introduce(self) -> str:
        return f"Chatting about URL {self.url}"

    def activate(self, prompt_section: Optional[UserPromptSection] = None) -> bool:
        if super().activate():
            user_input = prompt_section.prompt if prompt_section else None
            user_input_trimmed = user_input.strip() if user_input else None

            if not prompt_section.prompt:
                self.assistant.log(f"Please provide a URL")
                return False

            if not validators.url(prompt_section.prompt):
                self.assistant.log(f"Provided URL is not valid: {prompt_section.prompt}")
                return False

            self.url = user_input_trimmed
            return True

        return False
