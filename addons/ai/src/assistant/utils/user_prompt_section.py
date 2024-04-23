from typing import Optional, List


class UserPromptSection(object):
    command: Optional[str]
    prompt: Optional[str]

    def __init__(self, command: Optional[str], prompt: Optional[str], options: Optional[List[str]] = None) -> None:
        self.command = command
        self.prompt = prompt
        self.options = options or []
