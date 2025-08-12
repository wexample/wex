from addons.ai.src.assistant.command.abstract_command import AbstractCommand


class ExitCommand(AbstractCommand):
    description: str = "Exit from talk"

    @staticmethod
    def name() -> str:
        return "exit"
