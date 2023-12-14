from addons.app.const.app import APP_DIR_APP_DATA, APP_ENV_PROD
from src.core.file.AbstractFileSystemStructure import FileSystemStructureSchema
from src.core.file.DirectoryStructure import DirectoryStructure


class AppDirectoryStructure(DirectoryStructure):
    schema: FileSystemStructureSchema = {
        APP_DIR_APP_DATA: {
            "should_exist": True,
            "schema": {
                "tmp": {
                    "should_exist": True,
                    "on_missing": "create",
                },
                ".env": {
                    "type": "file",
                    "should_exist": True,
                    "on_missing": "create",
                    "default_content": f"APP_ENV={APP_ENV_PROD}",
                },
            },
        }
    }
