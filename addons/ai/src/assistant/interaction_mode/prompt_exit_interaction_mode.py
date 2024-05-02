from ai.src.assistant.interaction_mode.abstract_interaction_mode import AbstractInteractionMode


class PromptExitInteractionMode(AbstractInteractionMode):
    @staticmethod
    def name() -> str:
        return "exit"
