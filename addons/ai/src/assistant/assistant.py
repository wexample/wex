import os
from typing import TYPE_CHECKING, Dict, List, Optional, cast

import psycopg2
from prompt_toolkit import HTML, print_formatted_text

from addons.ai.src.assistant.prompt_manager import PromptManager
from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from addons.ai.src.assistant.subject.agent_chat_subject import AgentChatSubject
from addons.ai.src.assistant.subject.default_chat_subject import DefaultChatSubject
from addons.ai.src.assistant.subject.file_chat_subject import FileChatSubject
from addons.ai.src.assistant.subject.function_chat_subject import FunctionChatSubject
from addons.ai.src.assistant.subject.help_chat_subject import HelpChatSubject
from addons.ai.src.assistant.subject.investigate_chat_subject import InvestigateChatSubject
from addons.ai.src.assistant.utils.globals import (
    ASSISTANT_DEFAULT_COMMANDS,
    CHAT_MENU_ACTION_CHAT,
    CHAT_MENU_ACTION_CHANGE_DEFAULT_MODEL,
    CHAT_MENU_ACTION_THEME,
    CHAT_MENU_ACTION_EXIT,
    CHAT_MENU_ACTIONS_TRANSLATIONS,
    AI_COMMAND_PREFIX,
    ASSISTANT_COMMAND_MENU,
    ASSISTANT_COMMAND_EXIT,
    CHAT_MENU_ACTION_CHANGE_PERSONALITY,
    CHAT_MENU_ACTION_CHANGE_LANGUAGE,
)
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from addons.ai.src.model.abstract_model import AbstractModel
from addons.ai.src.model.ollama_model import MODEL_NAME_OLLAMA_MISTRAL, OllamaModel
from addons.ai.src.model.open_ai_model import (
    MODEL_NAME_OPEN_AI_GPT_3_5_TURBO,
    MODEL_NAME_OPEN_AI_GPT_4,
    OpenAiModel,
)
from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.helper.start import app__helper__start
from addons.app.const.app import HELPER_APP_AI_SHORT_NAME
from src.const.types import StringKeysDict
from src.core.KernelChild import KernelChild
from src.core.spinner import Spinner
from src.helper.data_json import json_load
from src.helper.data_yaml import yaml_load
from src.helper.prompt import prompt_choice_dict, prompt_progress_steps

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class Assistant(KernelChild):
    language: str
    subject: AbstractChatSubject
    _default_model: Optional[AbstractModel] = None

    def __init__(self, kernel: "Kernel", default_model: str) -> None:
        super().__init__(kernel)

        self._initial_default_model = default_model
        self.colors_theme: Optional[str] = None

        prompt_progress_steps(
            kernel,
            [
                self._init_helper,
                self._init_database,
                self._init_prompt,
                self._init_locales,
                self._init_commands,
                self._init_personalities,
                self._init_subjects,
                self._init_models,
            ],
        )

    def _init_helper(self) -> None:
        # Start AI helper app
        response = self.kernel.run_function(
            app__helper__start,
            {
                "name": HELPER_APP_AI_SHORT_NAME,
                "create-network": False,
            }
        )

        self.helper_app_dir = str(response.last())
        current_workdir = os.getcwd()

        self.assistant_app_manager = AppAddonManager(
            self.kernel,
            "assistant_app",
            str(response.last()),
        )

        # Correct workdir which changes due to app creation
        os.chdir(current_workdir)

    def _init_models(self) -> None:
        self._default_model: Optional[AbstractModel] = None
        self.models: Dict[str, AbstractModel] = {
            MODEL_NAME_OLLAMA_MISTRAL: OllamaModel(
                self,
                MODEL_NAME_OLLAMA_MISTRAL
            ),
            MODEL_NAME_OPEN_AI_GPT_3_5_TURBO: OpenAiModel(
                self,
                MODEL_NAME_OPEN_AI_GPT_3_5_TURBO
            ),
            MODEL_NAME_OPEN_AI_GPT_4: OpenAiModel(
                self,
                MODEL_NAME_OPEN_AI_GPT_4
            ),
        }

        self.set_default_model(self._initial_default_model)

    def _init_prompt(self) -> None:
        self.prompt_manager = PromptManager(self)
        self.spinner = Spinner()

    def _init_commands(self) -> None:
        self.commands = ASSISTANT_DEFAULT_COMMANDS

    def _init_locales(self) -> None:
        self.languages = json_load(f"{self.kernel.directory.path}addons/ai/samples/languages.json")
        self.language = "en"
        self.set_language(self.language)

    def set_language(self, code: str):
        self.language = code

    def _init_subjects(self) -> None:
        subjects = [
            FileChatSubject,
            HelpChatSubject,
            AgentChatSubject,
            InvestigateChatSubject,
            FunctionChatSubject,
            # Should be last, as fallback
            DefaultChatSubject,
        ]

        self.subjects: Dict[str, AbstractChatSubject] = {}
        for subject_class in subjects:
            subject = cast(AbstractChatSubject, subject_class(self))
            self.subjects[subject.name()] = subject

        self.set_default_subject()

    def _init_personalities(self) -> None:
        personalities_path = f"{self.kernel.directory.path}addons/ai/samples/personalities/"
        personalities = {}

        # Scan the directory for files and load their contents
        for filename in os.listdir(personalities_path):
            if filename.endswith(".yml"):
                name_without_extension, _ = os.path.splitext(filename)
                personalities[name_without_extension] = yaml_load(os.path.join(personalities_path, filename))

        self.personality: str = "default"
        self.personalities = personalities

    def _init_database(self) -> None:
        database_config = self.assistant_app_manager.get_config("service.postgres").get_dict()

        conn = psycopg2.connect(
            dbname=database_config["name"],
            user=database_config["user"],
            password=database_config["password"],
            host="localhost",
            port=5444
        )

        self.db_cursor = conn.cursor()
        self.log("Database connected")

    def set_default_subject(self) -> None:
        self.set_subject(DefaultChatSubject.name())

    def set_subject(self, name: str, prompt_section: Optional[UserPromptSection] = None) -> AbstractChatSubject:
        subject = cast(AbstractChatSubject, self.subjects[name])

        if subject.activate(prompt_section):
            self.log("Setting subject: " + subject.introduce())
            self.subject = subject
        else:
            self.log("Failed to activate subject: " + name)

        return subject

    def get_current_subject(self) -> AbstractChatSubject:
        self._validate__should_not_be_none(self.subject)
        assert isinstance(self.subject, AbstractChatSubject)

        return self.subject

    def log(self, message: str) -> None:
        self.kernel.io.log(f"  {message}")

    def set_default_model(self, identifier: str) -> None:
        self.log(f"Model set to : {identifier}")

        self._default_model = self.models[identifier]

    def get_model(self, name: Optional[str] = None) -> AbstractModel:
        model = self.models[name] if name else self._default_model
        self._validate__should_not_be_none(model)
        assert isinstance(model, AbstractModel)

        if not model.activated:
            model.activate()

        return model

    def start(self, menu_action: Optional[str] = None) -> None:
        asked_exit = False
        while not asked_exit:
            if not menu_action:
                menu_action = self.show_menu()

            if menu_action == CHAT_MENU_ACTION_CHAT:
                # Reset default subject.
                self.set_default_subject()
                menu_action = self.chat()
            elif menu_action == CHAT_MENU_ACTION_CHANGE_LANGUAGE:
                self.language = prompt_choice_dict(
                    "Choose a language",
                    self.languages,
                    default=self.language,
                    abort="↩ Back"
                )

                menu_action = None
            elif menu_action == CHAT_MENU_ACTION_THEME:
                from pygments.styles._mapping import STYLES

                choice_dict = {}
                for key, value in STYLES.items():
                    style_name = value[1]
                    class_name = key[:-5]
                    choice_dict[style_name] = class_name

                self.colors_theme = prompt_choice_dict(
                    "Choose a theme:",
                    choice_dict,
                    default=self.colors_theme,
                    abort="↩ Back"
                )

                menu_action = None
            elif menu_action == CHAT_MENU_ACTION_CHANGE_PERSONALITY:
                choice_dict = {}
                for key, personality in self.personalities.items():
                    choice_dict[key] = personality["summary"]

                self.personality = prompt_choice_dict(
                    "Choose a personality:",
                    choice_dict,
                    default=self.personality,
                    abort="↩ Back"
                )

                menu_action = None
            elif menu_action == CHAT_MENU_ACTION_CHANGE_DEFAULT_MODEL:
                current_model = self.get_model()
                models = {}
                for model in self.models:
                    models[model] = model

                new_model = prompt_choice_dict(
                    "Choose a new language model:",
                    models,
                    default=current_model.identifier,
                    abort="↩ Back"
                )

                menu_action = None

                self.set_default_model(new_model)

            if menu_action == CHAT_MENU_ACTION_EXIT:
                asked_exit = True

        self.log(f"{os.linesep}Ciao")

    def show_menu(self) -> Optional[str]:
        # List of all possible menu actions
        menu_actions = [
            CHAT_MENU_ACTION_CHAT,
            CHAT_MENU_ACTION_THEME,
            CHAT_MENU_ACTION_CHANGE_LANGUAGE,
            CHAT_MENU_ACTION_CHANGE_PERSONALITY,
            CHAT_MENU_ACTION_CHANGE_DEFAULT_MODEL,
            CHAT_MENU_ACTION_EXIT
        ]

        # Initialize choices dictionary using a dictionary comprehension
        choices = {action: CHAT_MENU_ACTIONS_TRANSLATIONS[action] for action in menu_actions}

        # Prompt the user to choose an action
        action = prompt_choice_dict(
            "Menu:",
            choices,
            abort=None,
            default=CHAT_MENU_ACTION_CHAT,
        )

        # Return the chosen action as a string or None if aborted
        return str(action) if action else None

    def split_user_input_commands(self, user_input: str) -> List[UserPromptSection]:
        user_input = user_input.strip()
        # Special case if user types just "exit" without prefix.
        if user_input.lower() == "exit":
            return [UserPromptSection("exit", None)]

        results: List[UserPromptSection] = []
        words = user_input.split()
        commands = self.get_active_commands()

        for i, word in enumerate(words):
            if word.startswith(AI_COMMAND_PREFIX):
                command = word[len(AI_COMMAND_PREFIX):].lower()  # Remove prefix and normalize
                if command in commands:
                    # Find command input.
                    # Input is considered as the text following the command until the next command or end.
                    command_input = " ".join(words[i + 1:])  # Grab all text after command
                    # If another command is found in the input, cut the input at that point
                    next_command_index = next(
                        (j for j, w in enumerate(words[i + 1:], start=i + 1) if w.startswith(AI_COMMAND_PREFIX)), None)
                    if next_command_index:
                        command_input = " ".join(words[i + 1:next_command_index])

                    if command_input == "":
                        command_input = None

                    results.append(
                        UserPromptSection(command, command_input)
                    )

                    # Break after finding a command to avoid parsing further commands in the same string.
                    # If you need to handle multiple commands in one string, you might need a more complex approach.
                    break

        if not results:
            # No recognized command found
            return [UserPromptSection(None, user_input)]

        return results

    def get_active_commands(self) -> StringKeysDict:
        commands = self.commands.copy()

        for subject in self.subjects.values():
            commands.update(
                cast(AbstractChatSubject, subject).get_completer_commands()
            )

        return commands

    def chat(
        self,
        initial_prompt: Optional[str] = None,
    ) -> Optional[str]:
        cast(HelpChatSubject, self.subjects[HelpChatSubject.name()]).show_help()

        while True:
            try:
                if initial_prompt:
                    user_input = initial_prompt
                    initial_prompt = None
                else:
                    user_input = self.prompt_manager.open()

                user_input_splits = self.split_user_input_commands(user_input)
                result: Optional[str | bool] = None

                for index, prompt_section in enumerate(user_input_splits):
                    command = prompt_section.command

                    if command == ASSISTANT_COMMAND_EXIT:
                        return CHAT_MENU_ACTION_EXIT
                    elif command == ASSISTANT_COMMAND_MENU:
                        return None
                    else:
                        # Loop on subjects until one returns something.
                        for subject in self.subjects.values():
                            # Accepts "bool" return to block process without returning message.
                            if not result and subject.use_as_current_subject(prompt_section):
                                result = subject.interaction_mode.process_user_input(
                                    prompt_section,
                                    user_input_splits[index + 1:]
                                )

                    if isinstance(result, str):
                        self.print_ai(result)
            except KeyboardInterrupt:
                # User asked to quit
                if not self.spinner.running:
                    return CHAT_MENU_ACTION_EXIT
                # User asked to interrupt assistant.
                else:
                    self.spinner.stop()
                    self.kernel.io.print(os.linesep)

    def print_ai(self, message: str):
        # Let a new line separator
        print_formatted_text(HTML(f'✨ <ai fg="#9ABBD9">{message}</ai>'))
