from typing import Optional

from src.const.types import YamlContent
from src.core.file.FileStructure import FileStructure
from src.helper.data_yaml import yaml_load, yaml_write


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
