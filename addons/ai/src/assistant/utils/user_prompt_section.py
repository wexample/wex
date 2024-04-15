from typing import Optional


class UserPromptSection(object):
    command: Optional[str]
    prompt: Optional[str]

    def __init__(self, command: Optional[str], prompt: Optional[str]):
        self.command = command
        self.prompt = prompt
