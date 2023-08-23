
def merge_dicts(dict1, dict2):
    """
    Recursively merge two dictionaries.
    If a key exists in both dictionaries, the values are merged recursively.
    """
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result