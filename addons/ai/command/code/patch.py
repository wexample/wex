from addons.ai.src.assistant.AppAssistant import AppAssistant
from src.decorator.command import command
from src.decorator.option import option
from src.core import Kernel


@command(help="Ask assistant to patch project code")
@option('--question', '-q', type=str, required=True, help="Question")
def ai__code__patch(kernel: Kernel, question: str):
    assistant = AppAssistant(kernel)

    return assistant.patch(question)
