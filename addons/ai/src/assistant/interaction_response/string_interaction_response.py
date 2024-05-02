from addons.ai.src.assistant.interaction_response.abstract_interaction_response import AbstractInteractionResponse


class StringInteractionResponse(AbstractInteractionResponse):
    def __init__(self, string: str):
        self.string = string

    def render(self) -> str:
        return self.string
