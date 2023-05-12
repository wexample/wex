import argparse
import os
from typing import Optional

from src.helper.process import process_post_exec


class Kernel:
    path: dict[str, Optional[str]] = {
        'root': None,
        'addons': None
    }
    process_id: str = None

    def __init__(self, entrypoint_path):
        # Initialize global variables.
        self.path['root'] = os.path.dirname(os.path.realpath(entrypoint_path)) + '/'
        self.path['tmp'] = self.path['root'] + 'tmp/'

    def call(self):
        # Store pid.
        parser = argparse.ArgumentParser()
        parser.add_argument('--proc-id', type=str, help='The process ID')
        args = parser.parse_args()
        self.process_id = args.proc_id

        if not self.process_id:
            return

        process_post_exec(self, [
            'ls',
            '-la'
        ])

