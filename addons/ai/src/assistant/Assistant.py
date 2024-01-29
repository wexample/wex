import os
import time
from typing import TYPE_CHECKING, Dict, Optional

from prompt_toolkit import prompt as prompt_tool
from prompt_toolkit.completion import WordCompleter
from addons.ai.src.model.AbstractModel import AbstractModel
from addons.ai.src.model.OllamaModel import MODEL_NAME_OLLAMA_MISTRAL, OllamaModel
from addons.ai.src.model.OpenAiModel import MODEL_NAME_OPEN_AI_GPT_3_5_TURBO, MODEL_NAME_OPEN_AI_GPT_4, OpenAiModel
from addons.ai.src.tool.CommandTool import CommandTool
from src.helper.file import file_read
from src.const.types import StringKeysDict
from src.helper.dict import dict_merge, dict_sort_values
from src.helper.prompt import prompt_choice_dict
from src.helper.registry import registry_get_all_commands
from src.const.globals import COLOR_GRAY, COLOR_RESET

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

AI_IDENTITY_DEFAULT = "default"
AI_IDENTITY_CODE_FILE_PATCHER = "code_file_patcher"


class Assistant:
    def __init__(
        self, kernel: "Kernel", default_model: str = MODEL_NAME_OLLAMA_MISTRAL
    ) -> None:
        self.kernel = kernel
        self.model: Optional[AbstractModel] = None
        self.models: Dict[str, AbstractModel] = {
            MODEL_NAME_OLLAMA_MISTRAL: OllamaModel(self.kernel, MODEL_NAME_OLLAMA_MISTRAL),
            MODEL_NAME_OPEN_AI_GPT_3_5_TURBO: OpenAiModel(self.kernel, MODEL_NAME_OPEN_AI_GPT_3_5_TURBO),
            MODEL_NAME_OPEN_AI_GPT_4: OpenAiModel(self.kernel, MODEL_NAME_OPEN_AI_GPT_4),
        }

        self.set_model(default_model)
        self.completer = WordCompleter(["/action", "/?", "/exit"])

        # Create tools
        all_commands = registry_get_all_commands(self.kernel)
        self.tools = []

        self.identities = {
            AI_IDENTITY_DEFAULT: {
                "system": "You are a helpful AI bot."
            },
            AI_IDENTITY_CODE_FILE_PATCHER: {
                "system": "You are a helpful AI bot."
                          "\nNow we are talking about this file : {file_full_path}"
                          "\n_______________________________________File metadata"
                          "\nCreation Date: {file_creation_date}"
                          "\nFile Size: {file_size} bytes"
                          "\n_______________________________________File content"
                          "\n{file_content}"
                          "\n_________________________________________End of file info"
            }
        }

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

    def set_model(self, identifier: str):
        self.log(f"Model set to : {identifier}")

        self.model = self.models[identifier]
        self.model.activate()

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
                user_command = self.chat_about_file(os.getcwd())
            elif action == CHAT_ACTION_CHANGE_MODEL:
                models = {}
                for model in self.models:
                    models[model] = model

                new_model = prompt_choice_dict(
                    "Choose a new language model:", models, default=self.model.identifier
                )

                self.set_model(new_model)

            if user_command == "/exit":
                action = CHAT_ACTION_ABORT
            else:
                action = None

        self.log(f"{os.linesep}Ciao")

    def chat_about_file(self, base_dir: str) -> Optional[str]:
        # Use two dicts to keep dirs and files separated ignoring emojis in alphabetical sorting.
        choices_dirs = {
            "..": ".."
        }

        choices_files = {}

        for element in os.listdir(base_dir):
            if os.path.isdir(os.path.join(base_dir, element)):
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

        if file:
            full_path = os.path.join(base_dir, file)

            if os.path.isfile(file):
                self.log(f"File selected {full_path}")

                return self.user_prompt(
                    identity=AI_IDENTITY_CODE_FILE_PATCHER,
                    identity_parameters={
                        "file_full_path": full_path,
                        "file_creation_date": time.ctime(os.path.getctime(full_path)),
                        "file_size": os.path.getsize(full_path),
                        "file_content": file_read(full_path),
                    }
                )
            elif os.path.isdir(file):
                return self.chat_about_file(full_path)

        return None

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
        self,
        initial_prompt: Optional[str] = None,
        identity: str = AI_IDENTITY_DEFAULT,
        identity_parameters: Optional[StringKeysDict] = None,
    ) -> str:
        self.user_prompt_help()

        while True:
            ai_working = False

            try:
                if not initial_prompt:
                    input = prompt_tool(">>> ", completer=self.completer)
                    user_input_lower = input.strip().lower()

                    if user_input_lower == "exit":
                        user_input_lower = "/exit"

                    if user_input_lower in ["/exit", "/action"]:
                        return user_input_lower
                else:
                    input = user_input_lower = initial_prompt
                    initial_prompt = None

                if user_input_lower in ["/?", "/help"]:
                    self.user_prompt_help()
                else:
                    self.log("..")

                    self.kernel.io.print(COLOR_GRAY, end="")
                    ai_working = True

                    command_selection = self.model.choose_command(input)

                    if "text" in command_selection and command_selection["text"]:
                        # TODO Do command
                        self.kernel.io.print(command_selection["text"]["command"])
                    else:
                        result = self.model.request(
                            input,
                            self.identities[identity],
                            identity_parameters
                        )

                        # Let a new line separator
                        self.kernel.io.print(COLOR_RESET)

                        self.kernel.io.print(
                            result
                        )

            except KeyboardInterrupt:
                # User asked to quit
                if not ai_working:
                    return "/exit"
                # User asked to interrupt assistant.
                else:
                    self.kernel.io.print(os.linesep)
