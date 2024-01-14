from typing import TYPE_CHECKING

from addons.ai.src.assistant.AppAssistant import AppAssistant
from src.decorator.option import option
from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.alias import alias
from addons.app.decorator.app_command import app_command

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@alias("talk")
@app_command(help="Validate the code of current application", command_type=COMMAND_TYPE_ADDON)
@option('--question', '-q', type=str, required=True, help="Question or message")
def ai__talk__ask(manager: "AppAddonManager", app_dir: str, question: str):
    assistant = AppAssistant(manager)

    return assistant.assist(question)
