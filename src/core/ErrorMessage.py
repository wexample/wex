from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.const.types import StringMessageParameters


class ErrorMessage(Exception):
    def __init__(
        self, code: str, parameters: "StringMessageParameters", message: str
    ) -> None:
        self.code: str = code
        self.parameters: "StringMessageParameters" = parameters
        self.message: str = message


ErrorMessageList = List[ErrorMessage]
