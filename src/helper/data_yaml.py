from typing import Any, Optional, TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from src.const.types import YamlContent


def yaml_is_basic_data(value: str | int | float | bool | None) -> bool:
    """
    Check if the value is compatible with basic YAML types
    """

    yaml_basic_types = (str, int, float, bool, type(None))

    if isinstance(value, yaml_basic_types):
        return True

    elif isinstance(value, list):
        return all(yaml_is_basic_data(item) for item in value)

    elif isinstance(value, dict):
        return all(isinstance(key, str) and yaml_is_basic_data(val) for key, val in value.items())

    else:
        return False


def yaml_load(file_path: str, default: Optional['YamlContent'] = None) -> Optional['YamlContent']:
    try:
        with open(file_path, 'r') as f:
            content = yaml.safe_load(f)

            if isinstance(content, dict):
                return content
            else:
                return default
    except Exception:
        return default


def yaml_write(file_path: str, content: 'YamlContent') -> None:
    try:
        with open(file_path, 'w') as f:
            yaml.safe_dump(
                content,
                f)
    except Exception:
        return None


def yaml_load_or_default(file: str, default: Optional[Any] = None) -> Any:
    data_yaml = yaml_load(file)

    if data_yaml is None:
        return default or {}

    return data_yaml
