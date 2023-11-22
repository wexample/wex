from typing import Dict, Any
from src.core.file.DirectoryStructure import DirectoryStructure


class KernelDirectoryStructure(DirectoryStructure):
    schema: Dict[str, Dict[str, Any]] = {
        '.': {
            'should_exist': True,
            'initial_checkup': True,
        },
        'addons': {
            'should_exists': True,
        },
        'cli': {
            'should_exist': True,
            'children': {
                'wex': {
                    'name': 'cli',
                    'type': 'file',
                }
            }
        },
        'tmp': {
            'should_exist': True,
            'on_missing': 'create',
            'children': {
                'task': {
                    'on_missing': 'create',
                }
            }
        },
    }
