from typing import Optional

from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from src.const.types import StringKeysDict


class DefaultSubject(AbstractChatSubject):
    @staticmethod
    def name() -> str:
        return "default"

    def process_user_input(
        self,
        user_input_split: StringKeysDict,
        identity: StringKeysDict,
        identity_parameters: StringKeysDict,
    ) -> Optional[str]:
        self.assistant.spinner.start()

        response = self.assistant.get_default_model().chat(
            user_input_split["input"],
            identity,
            identity_parameters or {},
        )

        self.assistant.spinner.stop()

        return response
