from typing import Optional

from src.helper.data_yaml import yaml_load, YamlContent, yaml_write
from src.core.file.FileStructure import FileStructure


class YmlFileStructure(FileStructure):
    file_extension: str = 'yml'
    content: YamlContent

    def load_content(self, default: Optional[YamlContent] = None) -> YamlContent:
        self.content = yaml_load(self.path) or default

        return self.content

    def write_content(self) -> None:
        yaml_write(
            self.path,
            self.content
        )
