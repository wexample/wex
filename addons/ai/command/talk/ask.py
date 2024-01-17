import os
from typing import TYPE_CHECKING

from addons.ai.src.assistant.AppAssistant import AppAssistant
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_ADDON, CORE_COMMAND_NAME
from src.decorator.alias import alias

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@alias("talk")
@app_command(
    help="Validate the code of current application", command_type=COMMAND_TYPE_ADDON
)
def ai__talk__ask(manager: "AppAddonManager", app_dir: str) -> None:
    assistant = AppAssistant(manager)
    manager.kernel.io.message("Welcome to chat mode, type 'exit' to quit.")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit"]:
                manager.kernel.io.log(f"{os.linesep}Ciao")
                break
            response = assistant.assist(user_input)["text"].strip()
            manager.kernel.io.print(
                f"{os.linesep}{CORE_COMMAND_NAME}: {response}{os.linesep}"
            )
        except KeyboardInterrupt:
            manager.kernel.io.log(f"{os.linesep}Ciao")
            break
