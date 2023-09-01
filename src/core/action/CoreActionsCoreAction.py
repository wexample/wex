from src.core.action.AbstractCoreAction import AbstractCoreAction


class CoreActionsCoreAction(AbstractCoreAction):
    @staticmethod
    def command() -> str:
        return 'core-actions'

    def exec(self, command, command_args):
        return "\n".join(self.kernel.core_actions.keys())
