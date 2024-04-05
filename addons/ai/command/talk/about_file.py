from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.command import command
from src.decorator.option import option
from typing import TYPE_CHECKING
from addons.ai.src.assistant.Assistant import Assistant
from addons.ai.src.model.OpenAiModel import MODEL_NAME_OPEN_AI_GPT_4

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Description", command_type=COMMAND_TYPE_ADDON)
@option('--file', '-f', type=str, required=True, help="File path")
def ai__talk__about_file(kernel: "Kernel", file: str) -> None:
    assistant = Assistant(kernel, MODEL_NAME_OPEN_AI_GPT_4)

    assistant.chat_about_file(file)
