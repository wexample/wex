from src.core.file.AbstractFileSystemStructure import FileSystemStructureSchema
from src.core.file.DirectoryStructure import DirectoryStructure


class KernelSystemRootDirectoryStructure(DirectoryStructure):
    should_exist: bool = True

    def __init__(self, env: str, path: str, initialize: bool = True) -> None:
        self.env = env

        super().__init__(path, initialize)

    def get_schema(self) -> FileSystemStructureSchema:
        schema = super().get_schema()

        schema.update(
            {
                "var": {
                    "schema": {
                        "www": {
                            "schema": {
                                self.env: {
                                    "shortcut": "apps",
                                    "type": "dir",
                                    "on_missing": "create",
                                },
                            },
                        },
                    },
                },
            }
        )

        return schema
