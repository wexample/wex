import os

from addons.app.const.app import APP_DIR_APP_DATA_NAME, APP_ENV_PROD, APP_FILE_APP_ENV, APP_FILE_APP_CONFIG
from src.helper.data_yaml import yaml_load
from src.core.file.AbstractFileSystemStructure import FileSystemStructureSchema
from src.core.file.DirectoryStructure import DirectoryStructure


class AppDirectoryStructure(DirectoryStructure):
    def get_schema(self) -> FileSystemStructureSchema:
        schema = {
            APP_DIR_APP_DATA_NAME: {
                "should_exist": True,
                "schema": {
                    "tmp": {
                        "should_exist": True,
                        "on_missing": "create",
                    },
                    APP_FILE_APP_ENV: {
                        "type": "file",
                        "should_exist": True,
                        "on_missing": "create",
                        "default_content": f"APP_ENV={APP_ENV_PROD}",
                    },
                    APP_FILE_APP_CONFIG: {
                        "type": "file",
                        "should_exist": True,
                        "on_missing": "create",
                        "default_content": "global:",
                    },
                },
            }
        }

        config_file = os.path.join(self.path, APP_DIR_APP_DATA_NAME, APP_FILE_APP_CONFIG)

        config = yaml_load(config_file)
        if config and "structure" in config:
            schema.update(config["structure"])

        return schema
