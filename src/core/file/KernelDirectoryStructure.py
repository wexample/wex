from addons.app.src.file.AppDirectoryStructure import AppDirectoryStructure
from src.const.globals import CORE_COMMAND_NAME
from src.core.file.AbstractFileSystemStructure import FileSystemStructureSchema


class KernelDirectoryStructure(AppDirectoryStructure):
    should_exist: bool = True
    
    def get_schema(self) -> FileSystemStructureSchema:
        schema = super().get_schema()

        schema.update({
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
        })

        return schema
