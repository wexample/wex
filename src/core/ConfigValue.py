from typing import Any

from src.core.BaseClass import BaseClass

class ConfiValue(BaseClass):
    def __init__(self, kernel: "Kernel", value:Any) -> None:
        super().__init__(kernel)

        self._value: str = value

    def set_value(self) -> Any:
        self._validate__should_not_be_none(self._value)
        return self._value
