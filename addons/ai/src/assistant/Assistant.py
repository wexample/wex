import os
from typing import TYPE_CHECKING, Dict, Optional

from langchain.agents import AgentExecutor, create_react_agent
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from prompt_toolkit import prompt as prompt_tool
from prompt_toolkit.completion import WordCompleter

from addons.ai.src.model.AbstractModel import AbstractModel
from addons.ai.src.model.DefaultModel import MODEL_NAME_MISTRAL, DefaultModel
from addons.ai.src.model.OpenAiModel import MODEL_NAME_OPEN_AI, OpenAiModel
from addons.ai.src.tool.CommandTool import CommandTool
from src.const.globals import CORE_COMMAND_NAME
from src.const.types import StringKeysDict
from src.helper.dict import dict_merge, dict_sort_values
from src.helper.prompt import prompt_choice_dict
from src.helper.registry import registry_get_all_commands

if TYPE_CHECKING:
    from src.core.Kernel import Kernel

CHAT_ACTION_ABORT = "ABORT"
CHAT_ACTION_CHANGE_MODEL = "CHANGE_MODEL"
CHAT_ACTION_FREE_TALK = "FREE_TALK"
CHAT_ACTION_FREE_TALK_FILE = "TALK_FILE"
CHAT_ACTION_LAST = "ACTION_LAST"

CHAT_ACTIONS_TRANSLATIONS = {
    CHAT_ACTION_ABORT: "Abort",
    CHAT_ACTION_CHANGE_MODEL: "Change language model",
    CHAT_ACTION_FREE_TALK: "Free Talk",
    CHAT_ACTION_FREE_TALK_FILE: "Talk about a file",
    CHAT_ACTION_LAST: "Last action",
}


class Assistant:
    def __init__(
        self, kernel: "Kernel", default_model: str = MODEL_NAME_MISTRAL
    ) -> None:
        self.kernel = kernel
        self.model: Optional[AbstractModel] = None
        self.models: Dict[str, AbstractModel] = {
            MODEL_NAME_MISTRAL: DefaultModel(self.kernel, MODEL_NAME_MISTRAL),
            MODEL_NAME_OPEN_AI: OpenAiModel(self.kernel),
        }

        self.set_model(default_model)
        self.completer = WordCompleter(["/action", "/?", "/exit"])

        # Create tools
        all_commands = registry_get_all_commands(self.kernel)
        self.tools = []

        for command_name in all_commands:
            properties = all_commands[command_name]["properties"]

            if "ai_tool" in properties and properties["ai_tool"]:
                self.log(f"Loading tool {command_name}")

                command_tool = CommandTool(
                    self.kernel, command_name, all_commands[command_name]["description"]
                )

                self.tools.append(command_tool)

        self.log(f"Loaded {len(self.tools)} tools")

    def log(self, message):
        self.kernel.io.log(f"  {message}")

    def set_model(self, model_name: str):
        self.log(f"Model set to : {model_name}")

        self.model = self.models[model_name]
        self.model.activate()

    def react(self, question: str) -> StringKeysDict:
        prompt = PromptTemplate.from_file(
            f"{self.kernel.directory.path}addons/ai/samples/prompts/react.txt"
        )

        agent = create_react_agent(self.model.llm, self.tools, prompt=prompt)

        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

        return agent_executor.invoke({"input": question})["output"]

    def assist(self, question: str, system_prompt: Optional[str] = "") -> str:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI bot. Your name is {name} (allways lowercase)."
                    + (system_prompt or ""),
                ),
                ("human", "{user_input}"),
            ]
        )

        chain = LLMChain(
            llm=self.model.llm,
            prompt=prompt,
        )

        return chain.invoke({"name": CORE_COMMAND_NAME, "user_input": question})[
            "text"
        ].strip()

    def chat(self, initial_prompt: Optional[str] = None) -> None:
        action: Optional[str] = None
        previous_action: Optional[str] = None

        if initial_prompt:
            self.log(f"Prompt : {initial_prompt}")
            action = CHAT_ACTION_FREE_TALK

        while action != CHAT_ACTION_ABORT:
            if not action:
                action = self.chat_choose_action(previous_action)
                previous_action = action

            user_command = None
            if action == CHAT_ACTION_FREE_TALK:
                user_command = self.user_prompt(initial_prompt)
            elif action == CHAT_ACTION_FREE_TALK_FILE:
                dir = os.getcwd()
                # Use two dicts to keep dirs and files separated ignoring emojis in alphabetical sorting.
                choices_dirs = {}
                choices_files = {}

                for element in os.listdir(dir):
                    if os.path.isdir(os.path.join(dir, element)):
                        element_label = f"📁{element}"
                        choices_dirs[element] = element_label
                    else:
                        element_label = element
                        choices_files[element] = element_label

                choices_dirs = dict_sort_values(choices_dirs)
                choices_files = dict_sort_values(choices_files)

                file = prompt_choice_dict(
                    "Select a file to talk about:",
                    dict_merge(choices_dirs, choices_files),
                )

                if os.path.isfile(file):
                    selected_file = dir + file
                    self.log(f"File selected {selected_file}")

                    user_command = self.user_prompt(
                        system_prompt=f"Now we are talking about this file : {selected_file}"
                    )
            elif action == CHAT_ACTION_CHANGE_MODEL:
                models = {}
                for model in self.models:
                    models[model] = model

                new_model = prompt_choice_dict(
                    "Choose a new language model:", models, default=self.model.name
                )

                self.set_model(new_model)

            if user_command == "/exit":
                action = CHAT_ACTION_ABORT
            else:
                action = None

        self.log(f"{os.linesep}Ciao")

    def chat_choose_action(self, last_action: Optional[str]) -> str:
        choices = {
            CHAT_ACTION_FREE_TALK: CHAT_ACTIONS_TRANSLATIONS[CHAT_ACTION_FREE_TALK],
            CHAT_ACTION_FREE_TALK_FILE: CHAT_ACTIONS_TRANSLATIONS[
                CHAT_ACTION_FREE_TALK_FILE
            ],
        }

        if len(self.models.keys()) > 1:
            choices[CHAT_ACTION_CHANGE_MODEL] = CHAT_ACTIONS_TRANSLATIONS[
                CHAT_ACTION_CHANGE_MODEL
            ]

        if last_action:
            last_action_label = f"{CHAT_ACTIONS_TRANSLATIONS[CHAT_ACTION_LAST]} ({CHAT_ACTIONS_TRANSLATIONS[last_action]})"
            choices[CHAT_ACTION_LAST] = last_action_label

        choices[CHAT_ACTION_ABORT] = CHAT_ACTIONS_TRANSLATIONS[CHAT_ACTION_ABORT]

        return prompt_choice_dict(
            "Choose an action to do with ai assistant:",
            choices,
            abort=None,
            default=CHAT_ACTION_FREE_TALK,
        )

    def user_prompt_help(self) -> None:
        self.log("Type '/action' to pick an action.")
        self.log("Type '/?' or '/help' to display this message again.")
        self.log("Type '/exit' to quit.")

    def user_prompt(
        self, initial_prompt: Optional[str] = None, system_prompt: Optional[str] = None
    ) -> str:
        self.user_prompt_help()

        while True:
            ai_working = False

            try:
                if not initial_prompt:
                    user_input = prompt_tool(">>> ", completer=self.completer)
                    user_input_lower = user_input.lower()

                    if user_input_lower == "exit":
                        user_input_lower = "/exit"

                    if user_input_lower in ["/exit", "/action"]:
                        return user_input_lower
                else:
                    user_input = user_input_lower = initial_prompt
                    initial_prompt = None

                if user_input_lower in ["/?", "/help"]:
                    self.user_prompt_help()
                else:
                    self.log("..")
                    ai_working = True

                    self.kernel.io.print(
                        self.assist(user_input, system_prompt),
                    )

            except KeyboardInterrupt:
                # User asked to quit
                if not ai_working:
                    return "/exit"
                # User asked to interrupt assistant.
                else:
                    self.kernel.io.print(os.linesep)
