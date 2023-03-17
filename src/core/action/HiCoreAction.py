from src.core.action.AbstractCoreAction import AbstractCoreAction


class HiCoreAction(AbstractCoreAction):
    def exec(self, command, command_args):
        return 'hi!'
