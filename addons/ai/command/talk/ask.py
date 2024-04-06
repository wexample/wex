from typing import TYPE_CHECKING

from addons.ai.src.assistant.Assistant import Assistant, CHAT_ACTION_FREE_TALK
from addons.ai.src.model.OpenAiModel import MODEL_NAME_OPEN_AI_GPT_4
from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.alias import alias
from src.decorator.command import command
from src.decorator.option import option

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@alias("talk")
@command(
    help="Validate the code of current application", command_type=COMMAND_TYPE_ADDON
)
@option(
    "--model",
    "-m",
    type=str,
    required=True,
    default=MODEL_NAME_OPEN_AI_GPT_4,
    help="Default model",
)
def ai__talk__ask(kernel: "Kernel", model: str) -> None:
    assistant = Assistant(kernel, model)

    assistant.start(action=CHAT_ACTION_FREE_TALK)
