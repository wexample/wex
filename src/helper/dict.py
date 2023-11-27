import copy
from typing import Any, Dict, Mapping, Optional


def dict_merge(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively merge two dictionaries.
    If a key exists in both dictionaries, the values are merged recursively.
    """
    result = copy.deepcopy(dict1)
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = dict_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def dict_get_item_by_path(
    data: Mapping[str, Any], key: str, default: Optional[Any] = None
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


def dict_sort_values(dictionary: Mapping[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1])}
