from typing import Optional


class AbstractInteractionResponse(object):
    def render(self) -> Optional[str]:
        return None
