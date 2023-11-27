import json
import os
from typing import Any


def parse_json_if_valid(json_data: str) -> Any | bool:
    try:
        return json.loads(json_data)
    except json.JSONDecodeError:
        return False


def load_json_if_valid(path: str) -> Any | bool:
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return False
    return False
