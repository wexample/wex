from typing import Optional

from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from src.const.globals import COLOR_GRAY
from src.const.types import StringKeysDict


class DefaultSubject(AbstractChatSubject):
    def name(self) -> str:
        return "default"

    def process_user_input(
        self,
        user_input_split: StringKeysDict,
        identity: StringKeysDict,
        identity_parameters: StringKeysDict,
    ) -> Optional[str]:
        self.assistant.log("...")

        self.kernel.io.print(COLOR_GRAY, end="")
        self.assistant.ai_working = True

        return self.assistant.get_model().chat(
            user_input_split["input"],
            identity,
            identity_parameters or {},
        )
