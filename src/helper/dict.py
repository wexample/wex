import copy
from typing import Any, Optional

from src.const.types import StringKeysDict, StringKeysMapping


def dict_merge(*dicts):
    """
    Recursively merge multiple dictionaries.
    If a key exists in multiple dictionaries, the values are merged recursively.
    The function can take any number of dictionary arguments.
    """
    result = {}
    for dictionary in dicts:
        for key, value in dictionary.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = dict_merge(result[key], value)  # Recursively merge dicts
            else:
                result[key] = copy.deepcopy(value)
    return result


def dict_has_item_by_path(data: StringKeysMapping, key: str) -> bool:
    # Split the key into its individual parts
    keys = key.split(".")

    # Traverse the data dictionary using the key parts
    for k in keys:
        if k in data:
            data = data[k]
        else:
            return False

    return True


def dict_get_item_by_path(
    data: StringKeysMapping, key: str, default: Optional[Any] = None
) -> Any:
    # Split the key into its individual parts
    keys = key.split(".")

    # Traverse the data dictionary using the key parts
    for k in keys:
        if k in data:
            data = data[k]
        else:
            return default

    return data


def dict_sort_values(
    dictionary: StringKeysMapping, key: Optional[Any] = None
) -> StringKeysDict:
    return {
        k: v for k, v in sorted(dictionary.items(), key=key or (lambda item: item[1]))
    }
