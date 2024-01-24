from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from addons.ai.src.tool.CommandTool import CommandTool
from src.helper.registry import registry_get_all_commands
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class Assistant:
    def __init__(self, kernel: "Kernel") -> None:
        self.kernel = kernel

        self.llm = Ollama(
            model="mistral",
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
        )

        # Create tools
        all_commands = registry_get_all_commands(self.kernel)
        self.tools = []

        for command_name in all_commands:
            if ("ai_tool" in all_commands[command_name]["properties"]
                and all_commands[command_name]["properties"]["ai_tool"] == True):
                self.kernel.io.log(f"Loading tool {command_name}")

                command_tool = CommandTool(
                    self.kernel,
                    command_name,
                    all_commands[command_name]["description"]
                )

                self.tools.append(command_tool)

        self.kernel.io.log(f"Loaded {len(self.tools)} tools")
