from src.helper.data_yaml import yaml_load, YamlContent
from src.core.file.FileStructure import FileStructure


class YmlFileStructure(FileStructure):
    file_extension: str = 'yml'

    def load_content(self) -> YamlContent:
        self.content = yaml_load(self.path)

        return self.content
