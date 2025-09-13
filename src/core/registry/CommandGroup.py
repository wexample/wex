from __future__ import annotations

from src.core.registry.Command import RegistryCommand


class RegistryCommandGroup:
    commands: dict[str, RegistryCommand]

    def __init__(self) -> None:
        self.commands = {}
