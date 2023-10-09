from addons.ai.src.assistant.AppAssistant import AppAssistant
from src.decorator.command import command
from src.core import Kernel


@command(help="Description")
def ai__crawler__update(kernel: Kernel):
    assistant = AppAssistant(kernel)

    return assistant.crawler.build()
