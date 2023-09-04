import json
import os


def load_json_if_valid(path) -> bool:
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return False

    return False