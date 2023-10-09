from addons.ai.src.assistant.AppAssistant import AppAssistant
from src.decorator.command import command
from src.decorator.option import option
from src.core import Kernel


@command(help="Talk with assistant")
@option('--question', '-q', type=str, required=True, help="Question")
def ai__talk__ask(kernel: Kernel, question: str):
    assistant = AppAssistant(kernel)

    return assistant.assist(question)
