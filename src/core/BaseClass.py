from typing import Any


class BaseClass:
    def _validate__should_not_be_none(cls, value: Any) -> None:
        if value is None:
            raise ValueError("Property is not initialized")
        return value
