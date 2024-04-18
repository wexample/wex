import json
import os
from typing import Any, Union, List, Dict


def json_parse_if_valid(json_data: str) -> Any | bool:
    try:
        return json.loads(json_data)
    except json.JSONDecodeError:
        return False


def json_load_if_valid(path: str) -> Any | bool:
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return False
    return False


def json_load(path: str) -> Union[List[Any], Dict[Any, Any]]:
    with open(path, "r") as f:
        return json.load(f)
