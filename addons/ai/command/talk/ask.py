from typing import TYPE_CHECKING

from addons.ai.src.assistant.assistant import CHAT_MENU_ACTION_CHAT, Assistant
from addons.ai.src.model.open_ai_model import MODEL_NAME_OPEN_AI_GPT_4
from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.alias import alias
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from src.decorator.option import option

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@alias("talk")
@as_sudo()
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
@option(
    "--action",
    "-a",
    type=str,
    required=True,
    default=CHAT_MENU_ACTION_CHAT,
    help="Default action",
)
def ai__talk__ask(kernel: "Kernel", action: str, model: str) -> None:
    assistant = Assistant(kernel, model)

    assistant.start(menu_action=action)
