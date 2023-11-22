from typing import Dict, Any

from src.core.file.DirectoryStructure import DirectoryStructure


class KernelDirectoryStructure(DirectoryStructure):
    should_exist: bool = True
    checkup: bool = True
    children: Dict[str, Any] = {
        'addons': {
            'should_exists': True,
        },
        'cli': {
            'should_exist': True,
            'children': {
                'wex': {
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
