from typing import Dict

from src.core.registry.Command import RegistryCommand


class RegistryCommandGroup:
    commands: Dict[str, RegistryCommand]

    def __init__(self) -> None:
        self.commands = {}
