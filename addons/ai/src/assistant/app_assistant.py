from typing import TYPE_CHECKING

from addons.ai.src.assistant.assistant import Assistant
from src.const.types import StringKeysDict
from src.helper.file import file_read

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


class AppAssistant(Assistant):
    def __init__(self, manager: "AppAddonManager") -> None:
        super().__init__(manager.kernel)

        self.manager = manager

    def load_example_patch(self, name: str) -> StringKeysDict:
        base_path = f"{self.manager.get_app_dir()}.wex/command/samples/examples/{name}/"

        return {
            "prompt": file_read(f"{base_path}prompt.txt"),
            "source": file_read(f"{base_path}source.py"),
            "patch": file_read(f"{base_path}response.patch"),
            "tree": file_read(f"{base_path}tree.yml"),
        }
