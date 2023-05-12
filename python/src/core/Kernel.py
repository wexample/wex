import os
import datetime

from typing import Optional


class Kernel:
    path: dict[str, Optional[str]] = {
        'root': None,
        'addons': None
    }
    process_id: str = None

    def __init__(self, entrypoint_path, process_id=None):
        # Initialize global variables.
        self.path['root'] = os.path.dirname(os.path.realpath(entrypoint_path)) + '/'
        self.path['tmp'] = self.path['root'] + 'tmp/'

        self.process_id = (
            process_id
            if process_id is not None
            else f"{os.getpid()}.{datetime.datetime.now().strftime('%s.%f')}"
        )

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
