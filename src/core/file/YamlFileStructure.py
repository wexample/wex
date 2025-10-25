from __future__ import annotations

from typing import cast

from src.const.types import YamlContentDict
from src.core.file.FileStructure import FileStructure
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.const.types import YamlContent


class YamlFileStructure(FileStructure):
    content: YamlContent
    file_extension: str = "yml"

    def get_writable_content(self) -> YamlContent:
        from src.const.types import BasicValue
        from wexample_helpers.helpers.args import args_is_basic_value

        content = self.content
        args_is_basic_value(content)

        return cast(BasicValue, content)

    def load_content(self, default: YamlContentDict | None = None) -> None:
        self.content = self.load_content_yaml(default)

    def load_content_yaml(self, default: YamlContentDict | None = None) -> YamlContent:
        from wexample_helpers_yaml.helpers.yaml_helpers import yaml_read
        from src.const.types import YamlContent

        return cast(YamlContent, yaml_read(self.path) or default)

    def load_content_yaml_dict(
        self, default: YamlContentDict | None = None
    ) -> YamlContentDict:
        value = self.load_content_yaml(default)

        if not isinstance(value, dict):
            return {"value": value}

        return value

    def write_content(self) -> None:
        from wexample_helpers_yaml.helpers.yaml_helpers import yaml_write

        yaml_write(self.path, self.get_writable_content())
