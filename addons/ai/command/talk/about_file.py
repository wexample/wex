from typing import TYPE_CHECKING, cast

from addons.ai.src.assistant.assistant import Assistant
from addons.ai.src.assistant.subject.file_chat_subject import FileChatSubject
from addons.ai.src.model.open_ai_model import MODEL_NAME_OPEN_AI_GPT_4
from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.command import command
from src.decorator.option import option

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Description", command_type=COMMAND_TYPE_ADDON)
@option("--file", "-f", type=str, required=True, help="File path")
def ai__talk__about_file(kernel: "Kernel", file: str) -> None:
    assistant = Assistant(kernel, MODEL_NAME_OPEN_AI_GPT_4)

    subject = cast(FileChatSubject, assistant.set_subject(FileChatSubject.name()))
    subject.set_file_path(file)

    assistant.chat()
