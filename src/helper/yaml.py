def is_basic_yaml_data(value):
    """
    Check if the value is compatible with basic YAML types
    """

    yaml_basic_types = (str, int, float, bool, type(None))

    if isinstance(value, yaml_basic_types):
        return True

    elif isinstance(value, list):
        return all(is_basic_yaml_data(item) for item in value)

    elif isinstance(value, dict):
        return all(isinstance(key, str) and is_basic_yaml_data(val) for key, val in value.items())

    else:
        return False
