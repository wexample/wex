from src.core.action.AbstractCoreAction import AbstractCoreAction


class HiCoreAction(AbstractCoreAction):
    @staticmethod
    def command() -> str:
        return 'hi'

    def exec(self, command, command_args):
        return 'hi!'
