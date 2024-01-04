from typing import Optional

import yaml

from src.const.types import YamlContent, YamlContentDict


def yaml_load(
    file_path: str, default: Optional[YamlContent] = None
) -> Optional[YamlContent]:
    try:
        with open(file_path, "r") as f:
            content = yaml.safe_load(f)

            if isinstance(content, dict):
                return content
            else:
                return default
    except Exception:
        return default


def yaml_load_dict(
    file_path: str, default: Optional[YamlContentDict] = None
) -> YamlContentDict:
    content = yaml_load(file_path, default)

    if not content:
        return default or {}

    assert isinstance(content, dict)

    return content


def yaml_write(file_path: str, content: YamlContent) -> None:
    with open(file_path, "w") as f:
        yaml.safe_dump(content, f)
