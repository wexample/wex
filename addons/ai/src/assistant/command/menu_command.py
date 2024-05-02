from addons.ai.src.assistant.command.abstract_command import AbstractCommand


class MenuCommand(AbstractCommand):
    description: str = "Show menu"

    @staticmethod
    def name() -> str:
        return "menu"
