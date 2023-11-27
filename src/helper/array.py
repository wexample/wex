from typing import Any, List, Sequence


def array_unique(array: Sequence[Any]) -> List[Any]:
    return list(set(array))


def array_replace_value(
    array: Sequence[Any], search: Any, replacement: Any
) -> List[Any]:
    return [replacement if value == search else value for value in array]
