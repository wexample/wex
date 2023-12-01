from typing import Optional, cast

from src.const.types import BasicValue, YamlContent, YamlContentDict
from src.core.file.FileStructure import FileStructure
from src.helper.args import args_is_basic_value
from src.helper.data_yaml import yaml_load, yaml_write


class YamlFileStructure(FileStructure):
    file_extension: str = "yml"
    content: YamlContent

    def load_content_yaml_dict(
        self, default: Optional[YamlContentDict] = None
    ) -> YamlContentDict:
        value = self.load_content_yaml(default)

        if not isinstance(value, dict):
            return {"value": value}

        return value

    def load_content_yaml(
        self, default: Optional[YamlContentDict] = None
    ) -> YamlContent:
        return yaml_load(self.path) or default

    def load_content(self, default: Optional[YamlContentDict] = None) -> None:
        self.content = self.load_content_yaml(default)

    def write_content(self) -> None:
        yaml_write(self.path, self.get_writable_content())

    def get_writable_content(self) -> YamlContent:
        content = self.content
        args_is_basic_value(content)

        return cast(BasicValue, content)
