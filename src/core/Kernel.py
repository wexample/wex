import os
import sys
from typing import Optional


class Kernel:
    path: dict[str, Optional[str]] = {
        'root': None,
        'addons': None
    }

    def __init__(self, path_root):
        # Initialize global variables.
        self.path['root'] = os.path.dirname(os.path.realpath(path_root)) + '/'

    def call(self):
        if not len(sys.argv) > 3:
            return

        print('hi!')
