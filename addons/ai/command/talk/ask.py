from typing import TYPE_CHECKING, Optional

from addons.ai.src.assistant.Assistant import Assistant
from addons.ai.src.model.OllamaModel import MODEL_NAME_OLLAMA_MISTRAL
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
@option("--prompt", "-p", type=str, required=False, help="First prompt")
@option(
    "--model",
    "-m",
    type=str,
    required=True,
    default=MODEL_NAME_OLLAMA_MISTRAL,
    help="Default model",
)
def ai__talk__ask(kernel: "Kernel", model: str, prompt: Optional[str] = None) -> None:
    assistant = Assistant(kernel, model)

    assistant.chat(prompt)
