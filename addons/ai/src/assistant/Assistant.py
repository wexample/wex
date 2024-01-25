from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from addons.ai.src.tool.CommandTool import CommandTool
from src.helper.registry import registry_get_all_commands
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from src.const.types import StringKeysDict

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
            properties = all_commands[command_name]["properties"]

            if "ai_tool" in properties and properties["ai_tool"]:
                self.kernel.io.log(f"Loading tool {command_name}")

                command_tool = CommandTool(
                    self.kernel,
                    command_name,
                    all_commands[command_name]["description"]
                )

                self.tools.append(command_tool)

        self.kernel.io.log(f"Loaded {len(self.tools)} tools")

    def assist(self, question: str) -> StringKeysDict:
        prompt = PromptTemplate.from_file(f"{self.kernel.directory.path}addons/ai/samples/prompts/react.txt")

        agent = create_react_agent(
            self.llm,
            self.tools,
            prompt=prompt
        )

        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True)

        return agent_executor.invoke(
            {"input": question}
        )["output"]
