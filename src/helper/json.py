import json
import os


def parse_json_if_valid(json_data) -> dict | bool:
    try:
        return json.loads(json_data)
    except json.JSONDecodeError:
        return {}

def load_json_if_valid(path) -> dict | bool:
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return False

    return False
