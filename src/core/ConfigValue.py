from typing import Any

from src.core.BaseClass import BaseClass


class ConfigValue(BaseClass):
    def __init__(self, value: Any) -> None:
        self.set_value(value)

    def get_value(self) -> Any:
        self._validate__should_not_be_none(self._value)
        return self._value

    def set_value(self, value) -> None:
        self._value = value
