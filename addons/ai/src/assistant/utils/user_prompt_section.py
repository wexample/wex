from typing import List, Optional, Tuple

from addons.ai.src.assistant.command.abstract_command import AbstractCommand
from src.core.BaseClass import BaseClass


class UserPromptSection(BaseClass):
    command: Optional[AbstractCommand]
    prompt: Optional[str]

    def __init__(
        self,
        command: Optional[AbstractCommand],
        prompt: Optional[str],
        flags: Optional[List[str]] = None,
    ) -> None:
        self._command = command
        self.prompt = prompt
        self.flags = flags or []
        self.prompt_configurations: [Tuple[str, str]] = []

    def has_command(self) -> bool:
        return self._command is not None

    def get_command(self) -> AbstractCommand:
        self._validate__should_not_be_none(self._command)
        assert isinstance(self._command, AbstractCommand)

        return self._command
