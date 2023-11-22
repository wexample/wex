from src.core.file.KernelRegistryFileStructure import KernelRegistryFileStructure
from src.const.globals import CORE_COMMAND_NAME
from src.core.file.AbstractFileSystemStructure import FileSystemStructureSchema, \
    FILE_SYSTEM_SCHEMA_ITEM_KEY_SHOULD_EXIST, FILE_SYSTEM_SCHEMA_ITEM_KEY_SCHEMA, \
    FILE_SYSTEM_SCHEMA_ITEM_KEY_ON_MISSING, FILE_SYSTEM_TYPE_FILE, FILE_SYSTEM_SCHEMA_ITEM_KEY_TYPE, \
    FILE_SYSTEM_ACTION_ON_MISSING_CREATE, FILE_SYSTEM_SCHEMA_ITEM_KEY_CLASS, FILE_SYSTEM_SCHEMA_ITEM_KEY_SHORTCUT
from src.core.file.DirectoryStructure import DirectoryStructure


class KernelDirectoryStructure(DirectoryStructure):
    should_exist: bool = True
    schema: FileSystemStructureSchema = {
        'addons': {
            FILE_SYSTEM_SCHEMA_ITEM_KEY_SHOULD_EXIST: True,
        },
        'cli': {
            FILE_SYSTEM_SCHEMA_ITEM_KEY_SHOULD_EXIST: True,
            FILE_SYSTEM_SCHEMA_ITEM_KEY_SCHEMA: {
                CORE_COMMAND_NAME: {
                    FILE_SYSTEM_SCHEMA_ITEM_KEY_TYPE: FILE_SYSTEM_TYPE_FILE,
                    FILE_SYSTEM_SCHEMA_ITEM_KEY_SHOULD_EXIST: True,
                }
            }
        },
        'tmp': {
            FILE_SYSTEM_SCHEMA_ITEM_KEY_SHOULD_EXIST: True,
            FILE_SYSTEM_SCHEMA_ITEM_KEY_ON_MISSING: FILE_SYSTEM_ACTION_ON_MISSING_CREATE,
            FILE_SYSTEM_SCHEMA_ITEM_KEY_SCHEMA: {
                'task': {
                    FILE_SYSTEM_SCHEMA_ITEM_KEY_ON_MISSING: FILE_SYSTEM_ACTION_ON_MISSING_CREATE,
                },
                'registry.yml': {
                    FILE_SYSTEM_SCHEMA_ITEM_KEY_SHOULD_EXIST: True,
                    FILE_SYSTEM_SCHEMA_ITEM_KEY_CLASS: KernelRegistryFileStructure,
                    FILE_SYSTEM_SCHEMA_ITEM_KEY_SHORTCUT: 'registry'
                }
            }
        },
    }
