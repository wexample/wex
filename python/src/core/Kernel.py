import os
from typing import Optional


class Kernel:
    path: dict[str, Optional[str]] = {
        'root': None,
        'addons': None
    }

    def __init__(self, entrypoint_path):
        # Initialize global variables.
        self.path['root'] = os.path.dirname(os.path.realpath(entrypoint_path)) + '/'
        self.path['tmp'] = self.path['root'] + 'tmp/'

    def get_env_var(self, env_file_path, variable_name):
        with open(env_file_path, "r") as file:
            for line in file:
                key, value = line.strip().split("=", 1)
                if key == variable_name:
                    return value
        return None

    def get_env(self):
        return self.get_env_var(
            os.path.join(self.path['root'], ".wex", ".env"),
            "APP_ENV"
        )
