from __future__ import annotations


from addons.ai.src.assistant.command.abstract_command import AbstractCommand
from src.core.BaseClass import BaseClass


class UserPromptSection(BaseClass):
    command: AbstractCommand | None
    prompt: str | None

    def __init__(
        self,
        command: AbstractCommand | None,
        prompt: str | None,
        flags: list[str] | None = None,
    ) -> None:
        self._command = command
        self.prompt = prompt
        self.flags = flags or []
        self.prompt_configurations: list[tuple[str, str]] = []

    def has_command(self) -> bool:
        return self._command is not None

    def get_command(self) -> AbstractCommand:
        self._validate__should_not_be_none(self._command)
        assert isinstance(self._command, AbstractCommand)

        return self._command
