import os
from typing import cast

from addons.app.const.app import APP_DIR_APP_DATA_NAME, APP_ENV_PROD, APP_FILE_APP_ENV, APP_FILE_APP_CONFIG
from src.const.types import AppConfig, FileSystemStructureSchema
from src.helper.data_yaml import yaml_load
from src.core.file.DirectoryStructure import DirectoryStructure


class AppDirectoryStructure(DirectoryStructure):
    def __init__(self, path: str, initialize: bool = True, should_be_valid_app: bool = True) -> None:
        self.should_be_valid_app = should_be_valid_app

        super().__init__(path, initialize)

    def get_schema(self) -> FileSystemStructureSchema:
        schema:FileSystemStructureSchema = {
            APP_DIR_APP_DATA_NAME: {
                "should_exist": self.should_be_valid_app,
                "schema": {
                    "tmp": {
                        "should_exist": self.should_be_valid_app,
                        "on_missing": "create",
                    },
                    APP_FILE_APP_ENV: {
                        "type": "file",
                        "should_exist": self.should_be_valid_app,
                        "on_missing": "create",
                        "default_content": f"APP_ENV={APP_ENV_PROD}",
                    },
                    APP_FILE_APP_CONFIG: {
                        "type": "file",
                        "should_exist": self.should_be_valid_app,
                        "on_missing": "error",
                        "default_content": "global:",
                    },
                },
            }
        }

        config_file = os.path.join(self.path, APP_DIR_APP_DATA_NAME, APP_FILE_APP_CONFIG)

        yaml_data = yaml_load(config_file)
        if yaml_data:
            config = cast(AppConfig, yaml_data)

            if "structure" in config:
                schema.update(cast(FileSystemStructureSchema, config["structure"]))

        return schema
