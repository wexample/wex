from typing import Any, Optional

from src.core.BaseClass import BaseClass


class ConfigValue(BaseClass):
    def __init__(self, value: Any) -> None:
        self._value = None
        self.set_value(value)

    def get_value(self) -> Any:
        self._validate__should_not_be_none(self._value)
        return self._value

    def set_value(self, value) -> None:
        self._value = value

    def get_str(self) -> str:
        value = self.get_value()
        assert isinstance(value, str)

        return value

    def get_int(self) -> int:
        value = self.get_value()
        assert isinstance(value, int)

        return value

    def get_dict(self) -> dict:
        value = self.get_value()
        assert isinstance(value, dict)

        return value

    def get_list(self) -> list:
        value = self.get_value()
        assert isinstance(value, list)

        return value

    def get_float(self) -> float:
        value = self.get_value()
        assert isinstance(value, float)

        return value

    def get_bool(self) -> bool:
        value = self.get_value()
        assert isinstance(value, bool)

        return value
