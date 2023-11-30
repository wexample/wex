from src.const.globals import CORE_COMMAND_NAME
from src.core.file.AbstractFileSystemStructure import FileSystemStructureSchema
from src.core.file.DirectoryStructure import DirectoryStructure


class KernelDirectoryStructure(DirectoryStructure):
    should_exist: bool = True
    schema: FileSystemStructureSchema = {
        "addons": {
            "should_exist": True,
        },
        "cli": {
            "should_exist": True,
            "schema": {
                CORE_COMMAND_NAME: {
                    "type": "file",
                    "should_exist": True,
                }
            },
        },
        "tmp": {
            "shortcut": "tmp",
            "should_exist": True,
            "on_missing": "create",
            "schema": {
                "task": {
                    "on_missing": "create",
                },
            },
        },
    }
