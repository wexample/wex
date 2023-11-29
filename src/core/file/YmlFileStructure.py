from typing import Optional

from src.const.types import BasicInlineValue, BasicValue, StringKeysDict, YamlContent
from src.core.file.FileStructure import FileStructure
from src.helper.data_yaml import yaml_load, yaml_write


class YmlFileStructure(FileStructure):
    file_extension: str = "yml"
    content: YamlContent

    def load_content_yaml_dict(
        self, default: Optional[YamlContent] = None
    ) -> StringKeysDict:
        value = self.load_content_yaml()
        if isinstance(value, BasicInlineValue):
            return {"value": value}

        return yaml_load(self.path) or default

    def load_content_yaml(self, default: Optional[YamlContent] = None) -> YamlContent:
        return yaml_load(self.path) or default

    def load_content(self, default: Optional[YamlContent] = None) -> None:
        self.content = self.load_content_yaml(default)

    def write_content(self) -> None:
        yaml_write(self.path, self.get_writable_content())

    def get_writable_content(self) -> BasicValue:
        return self.content
