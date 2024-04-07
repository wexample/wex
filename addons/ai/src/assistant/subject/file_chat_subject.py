from typing import TYPE_CHECKING

from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class FileChatSubject(AbstractChatSubject):
    def name(self) -> str:
        return "file"

    def introduce(self) -> str:
        return f"Chatting about file {self.get_path()}"

    def __init__(self, file_path: str, kernel: "Kernel") -> None:
        super().__init__(kernel)
        self.file_path = file_path

    def get_path(self) -> str:
        self._validate__should_not_be_none(self.file_path)

        return self.file_path
