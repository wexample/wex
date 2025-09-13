from __future__ import annotations


class AbstractInteractionResponse:
    def render(self) -> str | None:
        return None
