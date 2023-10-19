import copy


def merge_dicts(dict1, dict2):
    """
    Recursively merge two dictionaries.
    If a key exists in both dictionaries, the values are merged recursively.
    """
    result = copy.deepcopy(dict1)
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def get_dict_item_by_path(data: dict, key: str, default=None):
    # Split the key into its individual parts
    keys = key.split('.')

    # Traverse the data dictionary using the key parts
    for k in keys:
        if k in data:
            data = data[k]
        else:
            return default

    return data


def dict_sort_values(dict: dict):
    return {k: v for k, v in sorted(dict.items(), key=lambda item: item[1])}
