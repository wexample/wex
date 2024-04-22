from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import AbstractInteractionMode


class DefaultInteractionMode(AbstractInteractionMode):
    @staticmethod
    def name() -> str:
        return "default"
