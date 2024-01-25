import os
from typing import TYPE_CHECKING, Optional

from addons.ai.helper.chat import TEXT_ALIGN_RIGHT, chat_format_message
from addons.ai.src.assistant.AppAssistant import AppAssistant
from src.decorator.command import command
from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.alias import alias
from src.decorator.option import option
from addons.ai.src.assistant.Assistant import Assistant

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@alias("talk")
@command(
    help="Validate the code of current application",
    command_type=COMMAND_TYPE_ADDON
)
@option('--prompt', '-p', type=str, required=False, help="First prompt")
@option('--model', '-m', type=str, required=True, default="mistral", help="Default model")
def ai__talk__ask(kernel: "Kernel", model: str, prompt: Optional[str] = None) -> None:
    assistant = Assistant(kernel, model)
    chat_help(kernel)

    def _quit() -> None:
        manager.kernel.io.log(f"{os.linesep}Ciao")

    while True:
        try:
            if not prompt:
                user_input = input(">>> ")
                if user_input.lower() in ["exit"]:
                    return chat_quit(kernel)
            else:
                user_input = prompt
                prompt = None

            kernel.io.print(
                chat_format_message(
                    assistant.assist(user_input),
                    TEXT_ALIGN_RIGHT
                )
            )
        except KeyboardInterrupt:
            return chat_quit(kernel)
