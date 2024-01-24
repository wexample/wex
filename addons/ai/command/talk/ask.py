import os
from typing import TYPE_CHECKING

from addons.ai.helper.chat import TEXT_ALIGN_RIGHT, chat_format_message
from addons.ai.src.assistant.AppAssistant import AppAssistant
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_ADDON
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

    def _quit() -> None:
        manager.kernel.io.log(f"{os.linesep}Ciao")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit"]:
                return _quit()

            manager.kernel.io.print(
                chat_format_message(
                    assistant.assist(user_input),
                    TEXT_ALIGN_RIGHT
                )
            )
        except KeyboardInterrupt:
            return _quit()
