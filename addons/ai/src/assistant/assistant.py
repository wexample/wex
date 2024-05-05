import html
import os
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, cast

from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from prompt_toolkit import HTML, print_formatted_text
from sqlalchemy import create_engine

from addons.ai.src.assistant.command.abstract_command import AbstractCommand
from addons.ai.src.assistant.command.agent_command import AgentCommand
from addons.ai.src.assistant.command.chat_command import ChatCommand
from addons.ai.src.assistant.command.default_command import DefaultCommand
from addons.ai.src.assistant.command.exit_command import ExitCommand
from addons.ai.src.assistant.command.format_command import FormatCommand
from addons.ai.src.assistant.command.help_command import HelpCommand
from addons.ai.src.assistant.command.menu_command import MenuCommand
from addons.ai.src.assistant.command.subject_command import SubjectCommand
from addons.ai.src.assistant.prompt_manager import PromptManager
from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from addons.ai.src.assistant.subject.default_chat_subject import DefaultChatSubject
from addons.ai.src.assistant.utils.globals import (
    AI_COMMAND_PREFIX,
    ASSISTANT_MENU_ACTION_CHANGE_DEFAULT_MODEL,
    ASSISTANT_MENU_ACTION_CHANGE_LANGUAGE,
    ASSISTANT_MENU_ACTION_CHANGE_PERSONALITY,
    ASSISTANT_MENU_ACTION_CHAT,
    ASSISTANT_MENU_ACTION_EXIT,
    ASSISTANT_MENU_ACTION_THEME,
    ASSISTANT_MENU_ACTIONS_TRANSLATIONS,
)
from addons.ai.src.assistant.utils.history_item import HistoryItem
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
from addons.ai.src.assistant.command.investigate_command import InvestigateCommand
from addons.ai.src.assistant.command.terminal_command import TerminalCommand
from addons.ai.src.assistant.command.function_command import FunctionCommand
from addons.ai.src.assistant.command.vet_command import VetCommand

from addons.ai.src.assistant.subject.file_chat_subject import FileChatSubject
from addons.ai.src.assistant.command.file_rewrite_command import FileRewriteCommand
from addons.ai.src.assistant.command.file_search_command import FileSearchCommand
from addons.ai.src.assistant.command.file_patch_command import FilePatchCommand
from addons.ai.src.assistant.subject.url_chat_subject import UrlChatSubject
from src.core.KernelChild import KernelChild
from src.core.spinner import Spinner
from src.helper.data_json import json_load
from src.helper.data_yaml import yaml_load
from src.helper.prompt import prompt_choice_dict, prompt_progress_steps

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class Assistant(KernelChild):
    language: str
    _default_model: Optional[AbstractModel] = None

    def __init__(self, kernel: "Kernel", default_model: str) -> None:
        super().__init__(kernel)

        self._initial_default_model = default_model
        self.colors_theme: Optional[str] = None
        self.history: List[HistoryItem] = []
        self.active_memory: Dict[Tuple[int, int], ChatMessageHistory] = {}
        self.user_id: int = 1
        self.conversation_id: int = 1
        self.subject: Optional[AbstractChatSubject] = None
        self.last_prompt_sections = None

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
            },
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
            MODEL_NAME_OLLAMA_MISTRAL: OllamaModel(self, MODEL_NAME_OLLAMA_MISTRAL),
            MODEL_NAME_OPEN_AI_GPT_3_5_TURBO: OpenAiModel(
                self, MODEL_NAME_OPEN_AI_GPT_3_5_TURBO
            ),
            MODEL_NAME_OPEN_AI_GPT_4: OpenAiModel(self, MODEL_NAME_OPEN_AI_GPT_4),
        }

        self.set_default_model(self._initial_default_model)

    def _init_prompt(self) -> None:
        self.prompt_manager = PromptManager(self)
        self.spinner = Spinner()

    def _init_commands(self) -> None:
        commands = [
            AgentCommand,
            ChatCommand,
            DefaultCommand,
            ExitCommand,
            FileRewriteCommand,
            FileSearchCommand,
            FilePatchCommand,
            FormatCommand,
            FunctionCommand,
            HelpCommand,
            InvestigateCommand,
            MenuCommand,
            SubjectCommand,
            TerminalCommand,
            VetCommand,
        ]

        self.commands: Dict[str, AbstractCommand] = {}
        for command_type in commands:
            self.commands[command_type.name()] = command_type(self)

    def _init_locales(self) -> None:
        self.languages = json_load(
            f"{self.kernel.directory.path}addons/ai/samples/languages.json"
        )
        self.language = "en"
        self.set_language(self.language)

    def set_language(self, code: str) -> None:
        self.language = code

    def _init_subjects(self) -> None:
        subjects = [
            DefaultChatSubject,
            FileChatSubject,
            UrlChatSubject
        ]

        self.subjects: Dict[str, AbstractChatSubject] = {}
        for subject_class in subjects:
            subject = cast(AbstractChatSubject, subject_class(self))
            self.subjects[subject.name()] = subject

        self.set_default_subject()

    def _init_personalities(self) -> None:
        personalities_path = (
            f"{self.kernel.directory.path}addons/ai/samples/personalities/"
        )
        personalities = {}

        # Scan the directory for files and load their contents
        for filename in os.listdir(personalities_path):
            if filename.endswith(".yml"):
                name_without_extension, _ = os.path.splitext(filename)
                personalities[name_without_extension] = yaml_load(
                    os.path.join(personalities_path, filename)
                )

        self.personality: str = "default"
        self.personalities = personalities

    def _init_database(self) -> None:
        manager = self.assistant_app_manager
        database_config = manager.get_config("service.postgres").get_dict()

        self.db_engine = create_engine(
            f"postgresql://{database_config['user']}"
            f":{database_config['password']}@localhost"
            f":5{manager.get_config('port.public', 444).get_int()}/{database_config['name']}"
        )

        self.log("Database connected")

    def set_default_subject(self) -> None:
        if not isinstance(self.subject, DefaultChatSubject):
            self.set_subject(DefaultChatSubject.name())

    def set_subject(self, name: str) -> AbstractChatSubject:
        subject = cast(AbstractChatSubject, self.subjects[name])

        self.subject = subject
        self.subject.activate()
        self.log("[subject] " + subject.introduce())

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

    def start(self, menu_action: str) -> None:
        asked_exit = False

        # Reset default subject.
        if not self.subject:
            self.set_default_subject()

        while not asked_exit:
            if not menu_action:
                menu_action = self.show_menu()

            if menu_action == ASSISTANT_MENU_ACTION_CHAT:
                menu_action = self.chat()
            elif menu_action == ASSISTANT_MENU_ACTION_CHANGE_LANGUAGE:
                self.language = prompt_choice_dict(
                    "Choose a language",
                    self.languages,
                    default=self.language,
                    abort="↩ Back",
                )

                menu_action = None
            elif menu_action == ASSISTANT_MENU_ACTION_THEME:
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
                    abort="↩ Back",
                )

                menu_action = None
            elif menu_action == ASSISTANT_MENU_ACTION_CHANGE_PERSONALITY:
                choice_dict = {}
                for key, personality in self.personalities.items():
                    choice_dict[key] = personality["summary"]

                self.personality = prompt_choice_dict(
                    "Choose a personality:",
                    choice_dict,
                    default=self.personality,
                    abort="↩ Back",
                )

                menu_action = None
            elif menu_action == ASSISTANT_MENU_ACTION_CHANGE_DEFAULT_MODEL:
                current_model = self.get_model()
                models = {}
                for model in self.models:
                    models[model] = model

                new_model = prompt_choice_dict(
                    "Choose a new language model:",
                    models,
                    default=current_model.identifier,
                    abort="↩ Back",
                )

                menu_action = None

                self.set_default_model(new_model)

            if menu_action == ASSISTANT_MENU_ACTION_EXIT:
                asked_exit = True

        self.log(f"{os.linesep}Ciao")

    def show_menu(self) -> Optional[str]:
        # List of all possible menu actions
        menu_actions = [
            ASSISTANT_MENU_ACTION_CHAT,
            ASSISTANT_MENU_ACTION_THEME,
            ASSISTANT_MENU_ACTION_CHANGE_LANGUAGE,
            ASSISTANT_MENU_ACTION_CHANGE_PERSONALITY,
            ASSISTANT_MENU_ACTION_CHANGE_DEFAULT_MODEL,
            ASSISTANT_MENU_ACTION_EXIT,
        ]

        # Initialize choices dictionary using a dictionary comprehension
        choices = {
            action: ASSISTANT_MENU_ACTIONS_TRANSLATIONS[action] for action in menu_actions
        }

        # Prompt the user to choose an action
        action = prompt_choice_dict(
            "Menu:",
            choices,
            abort=None,
            default=ASSISTANT_MENU_ACTION_CHAT,
        )

        # Return the chosen action as a string or None if aborted
        return str(action) if action else None

    def split_prompt_sections(self, user_input: str) -> List[UserPromptSection]:
        user_input = user_input.strip()
        # Special case if user types just "exit" without prefix.
        if user_input.lower() == ExitCommand.name():
            return [UserPromptSection(self.commands[ExitCommand.name()], None)]

        # Split on word to ensure commands is not attached to another word.
        results: List[UserPromptSection] = []
        words = user_input.split()
        commands = self.get_active_commands()

        for i, word in enumerate(words):
            if word.startswith(AI_COMMAND_PREFIX):
                # Split command and options
                command_parts = word[len(AI_COMMAND_PREFIX):].split(":")
                command = command_parts[
                    0
                ].lower()  # First part is the command, normalized
                options = (
                    command_parts[1:] if len(command_parts) > 1 else None
                )  # Subsequent parts are options

                if command in commands:
                    # Find command input.
                    # Input is considered as the text following the command until the next command or end.
                    command_input = " ".join(
                        words[i + 1:]
                    )  # Grab all text after command
                    # If another command is found in the input, cut the input at that point
                    next_command_index = next(
                        (
                            j
                            for j, w in enumerate(words[i + 1:], start=i + 1)
                            if w.startswith(AI_COMMAND_PREFIX)
                        ),
                        None,
                    )
                    if next_command_index:
                        command_input = " ".join(words[i + 1: next_command_index])

                    if command_input == "":
                        command_input = None
                    else:
                        command_input = html.unescape(command_input)

                    results.append(UserPromptSection(self.commands[command], command_input, options))

                    # Break after finding a command to avoid parsing further commands in the same string.
                    # If you need to handle multiple commands in one string, you might need a more complex approach.
                    break

        if not results:
            # No recognized command found
            return [UserPromptSection(None, user_input)]

        return results

    def get_active_commands(self) -> Dict[str, AbstractCommand]:
        commands = self.commands.copy()

        return commands

    def chat(
        self,
        initial_prompt: Optional[str] = None,
    ) -> Optional[str]:
        self.commands[HelpCommand.name()].execute()

        while True:
            try:
                if initial_prompt:
                    user_input = initial_prompt
                    initial_prompt = None
                else:
                    user_input = self.prompt_manager.open()

                prompt_sections = self.split_prompt_sections(user_input)

                for index, prompt_section in enumerate(prompt_sections):
                    if prompt_section.has_command():
                        command = prompt_section.get_command()

                        if isinstance(command, ExitCommand):
                            return ASSISTANT_MENU_ACTION_EXIT
                        elif isinstance(command, MenuCommand):
                            return None
                    else:
                        command = self.commands[DefaultCommand.name()]

                    self.history.append(HistoryItem(prompt_section.prompt))

                    result = command.execute(prompt_section, prompt_sections[index + 1:])
                    result_str = result.render()
                    self.history.append(HistoryItem(result_str))

                    if isinstance(result_str, str):
                        self.print_ai(result_str)

                self.last_prompt_sections = prompt_sections
            except KeyboardInterrupt:
                # User asked to quit
                if not self.spinner.running:
                    return ASSISTANT_MENU_ACTION_EXIT
                # User asked to interrupt assistant.
                else:
                    self.spinner.stop()
                    self.kernel.io.print(os.linesep)

    def print_ai(self, message: str) -> None:
        # Let a new line separator
        print_formatted_text(HTML(f'✨ <ai fg="#9ABBD9">{html.escape(message)}</ai>'))

    def get_current_session_history(self) -> BaseChatMessageHistory:
        return self.get_session_history(self.user_id, self.conversation_id)

    def get_session_history(
        self, user_id: int, conversation_id: int
    ) -> BaseChatMessageHistory:
        if (user_id, conversation_id) not in self.active_memory:
            self.active_memory[(user_id, conversation_id)] = ChatMessageHistory()

        return self.active_memory[(user_id, conversation_id)]

    def text_has_a_command(self, text: str) -> bool:
        sections = self.split_prompt_sections(text)
        return len(sections) and sections[-1].has_command()
