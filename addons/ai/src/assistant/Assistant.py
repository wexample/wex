from addons.ai.src.tool.CommandTool import CommandTool
from addons.ai.src.model.DefaultModel import DefaultModel, MODEL_NAME_MISTRAL
from addons.ai.src.model.OpenAiModel import OpenAiModel, MODEL_NAME_OPEN_AI
from addons.ai.src.model.AbstractModel import AbstractModel
from src.helper.registry import registry_get_all_commands
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from src.const.types import StringKeysDict

from typing import TYPE_CHECKING, cast, Any, Dict
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class Assistant:
    def __init__(self, kernel: "Kernel", default_model: str = MODEL_NAME_MISTRAL) -> None:
        self.kernel = kernel
        self.models: Dict[str, AbstractModel] = {
            MODEL_NAME_MISTRAL: DefaultModel(self.kernel, MODEL_NAME_MISTRAL),
            MODEL_NAME_OPEN_AI: OpenAiModel(self.kernel)
        }

        self.set_model(default_model)

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

    def set_model(self, model_name: str):
        self.model = self.models[model_name]
        self.model.activate()

    def react(self, question: str) -> StringKeysDict:
        prompt = PromptTemplate.from_file(f"{self.kernel.directory.path}addons/ai/samples/prompts/react.txt")

        agent = create_react_agent(
            self.model.llm,
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

    def assist(self, question: str) -> StringKeysDict:
        human_message_prompt = ChatPromptTemplate.from_template("{text}")

        prompt = ChatPromptTemplate.from_messages([human_message_prompt])

        chain = LLMChain(
            llm=self.model.llm,
            prompt=prompt,
        )

        return chain.invoke(
            cast(Any, question))["text"].strip()
