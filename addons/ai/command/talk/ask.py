from typing import TYPE_CHECKING

from addons.ai.src.assistant.AppAssistant import AppAssistant
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_ADDON
from src.const.typing import StringKeysDict
from src.decorator.alias import alias
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@alias("talk")
@app_command(
    help="Validate the code of current application", command_type=COMMAND_TYPE_ADDON
)
@option("--question", "-q", type=str, required=True, help="Question or message")
def ai__talk__ask(
    manager: "AppAddonManager", app_dir: str, question: str
) -> StringKeysDict:
    assistant = AppAssistant(manager)

    return assistant.assist(question)
