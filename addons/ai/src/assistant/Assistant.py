import os

from addons.ai.src.tool.CommandTool import CommandTool
from addons.ai.src.model.DefaultModel import DefaultModel, MODEL_NAME_MISTRAL
from addons.ai.src.model.OpenAiModel import OpenAiModel, MODEL_NAME_OPEN_AI
from addons.ai.src.model.AbstractModel import AbstractModel
from src.helper.registry import registry_get_all_commands
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from src.const.types import StringKeysDict
from addons.ai.helper.chat import TEXT_ALIGN_RIGHT, chat_format_message
from prompt_toolkit import prompt as prompt_tool
from typing import TYPE_CHECKING, cast, Any, Dict, Optional
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from src.helper.prompt import prompt_choice

if TYPE_CHECKING:
    from src.core.Kernel import Kernel

CHAT_ACTION_ABORT = "ABORT"
CHAT_ACTION_CHANGE_MODEL = "CHANGE_MODEL"
CHAT_ACTION_FREE_TALK = "FREE_TALK"
CHAT_ACTION_FREE_TALK_FILE = "TALK_FILE"
CHAT_ACTION_LAST = "ACTION_LAST"

CHAT_ACTIONS_TRANSLATIONS = {
    CHAT_ACTION_FREE_TALK: "> Free Talk",
    CHAT_ACTION_FREE_TALK_FILE: "> Talk about a file",
    CHAT_ACTION_LAST: "> Last action"
}


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

    def assist(self, question: str) -> str:
        human_message_prompt = ChatPromptTemplate.from_template("{text}")

        prompt = ChatPromptTemplate.from_messages([human_message_prompt])

        chain = LLMChain(
            llm=self.model.llm,
            prompt=prompt,
        )

        return chain.invoke(
            cast(Any, question))["text"].strip()

    def chat(self, initial_prompt: Optional[str] = None) -> None:
        action = self.chat_choose_action()

        if action == CHAT_ACTION_FREE_TALK:
            user_command = self.user_prompt(initial_prompt)

            if user_command == "/action":
                self.chat()
                return

        self.kernel.io.log(f"{os.linesep}Ciao")

    def chat_choose_action(self) -> str:
        choice = prompt_choice(
            "Choose an action to do with ai assistant :",
            [
                CHAT_ACTIONS_TRANSLATIONS[CHAT_ACTION_FREE_TALK],
                # CHAT_ACTIONS_TRANSLATIONS[CHAT_ACTION_FREE_TALK_FILE],
                # CHAT_ACTIONS_TRANSLATIONS[CHAT_ACTION_LAST],
            ],
        )

        return next((key for key, value in CHAT_ACTIONS_TRANSLATIONS.items() if value == choice), CHAT_ACTION_ABORT)

    def user_prompt_help(self) -> None:
        self.kernel.io.log("  Type '/action' to pick an action.")
        self.kernel.io.log("  Type '/?' or '/help' to display this message again.")
        self.kernel.io.log("  Type '/exit' to quit.")

    def user_prompt(self, initial_prompt: Optional[str]) -> str:
        self.kernel.io.message("Welcome to chat mode")
        self.user_prompt_help()

        while True:
            try:
                if not initial_prompt:
                    user_input = prompt_tool(">>> ")
                    user_input_lower = user_input.lower()

                    if user_input_lower in ["exit", "/exit", "/action"]:
                        return user_input_lower
                else:
                    user_input = user_input_lower = initial_prompt
                    initial_prompt = None

                if user_input_lower in ["/?", "/help"]:
                    self.user_prompt_help()
                else:
                    self.kernel.io.log("..")

                    self.kernel.io.print(
                        chat_format_message(
                            self.assist(user_input),
                            TEXT_ALIGN_RIGHT
                        )
                    )
            except KeyboardInterrupt:
                return "/exit"
