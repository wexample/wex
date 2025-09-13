from __future__ import annotations

from typing import Any

from src.const.types import AnyList, AppConfigValue, StringKeysDict
from src.core.BaseClass import BaseClass


class ConfigValue(BaseClass):
    def __init__(self, value: Any) -> None:
        self._value = None
        self.set_value(value)

    def get_bool(self) -> bool:
        value = self.get_value()
        assert isinstance(value, bool)

        return value

    def get_dict(self) -> StringKeysDict:
        value = self.get_value()
        assert isinstance(value, dict)

        return value

    def get_float(self) -> float:
        value = self.get_value()
        assert isinstance(value, float)

        return value

    def get_int(self) -> int:
        value = self.get_value()
        assert isinstance(value, int)

        return value

    def get_list(self) -> AnyList:
        value = self.get_value()
        assert isinstance(value, list)

        return value

    def get_str(self) -> str:
        value = self.get_value()
        assert isinstance(value, str)

        return value

    def get_value(self) -> AppConfigValue:
        self._validate__should_not_be_none(self._value)
        return self._value

    def is_bool(self) -> bool:
        return self.is_of_type(bool)

    def is_dict(self) -> bool:
        return self.is_of_type(dict)

    def is_float(self) -> bool:
        return self.is_of_type(float)

    def is_int(self) -> bool:
        return self.is_of_type(int)

    def is_list(self) -> bool:
        return self.is_of_type(list)

    def is_none(self) -> bool:
        return self._value is None

    def is_of_type(self, value_type: type) -> bool:
        return isinstance(self._value, value_type)

    def is_str(self) -> bool:
        return self.is_of_type(str)

    def set_value(self, value: Any) -> None:
        self._value = value
