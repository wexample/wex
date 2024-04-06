import os
import re
from typing import TYPE_CHECKING, Dict, Optional, cast

import chromadb
from langchain_community.vectorstores.chroma import Chroma
from prompt_toolkit import prompt as prompt_tool
from prompt_toolkit.completion import WordCompleter

from addons.ai.src.model.AbstractModel import AbstractModel
from addons.ai.src.model.OllamaModel import MODEL_NAME_OLLAMA_MISTRAL, OllamaModel
from addons.ai.src.model.OpenAiModel import (
    MODEL_NAME_OPEN_AI_GPT_3_5_TURBO,
    MODEL_NAME_OPEN_AI_GPT_4,
    OpenAiModel,
)
from addons.ai.src.tool.CommandTool import CommandTool
from addons.app.AppAddonManager import AppAddonManager
from src.const.globals import COLOR_GRAY, COLOR_RESET
from src.const.types import StringKeysDict
from src.core.BaseClass import BaseClass
from src.helper.dict import dict_merge, dict_sort_values
from src.helper.file import file_build_signature
from src.helper.prompt import prompt_choice_dict
from src.helper.registry import registry_get_all_commands

if TYPE_CHECKING:
    from src.core.Kernel import Kernel

CHAT_ACTION_EXIT = "EXIT"
CHAT_ACTION_CHANGE_MODEL = "CHANGE_MODEL"
CHAT_ACTION_FREE_TALK = "FREE_TALK"
CHAT_ACTION_FREE_TALK_FILE = "TALK_FILE"
CHAT_ACTION_LAST = "ACTION_LAST"

CHAT_ACTIONS_TRANSLATIONS = {
    CHAT_ACTION_EXIT: "Exit",
    CHAT_ACTION_CHANGE_MODEL: "Change language model",
    CHAT_ACTION_FREE_TALK: "Free Talk",
    CHAT_ACTION_FREE_TALK_FILE: "Talk about a file",
    CHAT_ACTION_LAST: "Last action",
}

AI_IDENTITY_DEFAULT = "default"
AI_IDENTITY_CODE_FILE_PATCHER = "code_file_patcher"
AI_IDENTITY_FILE_INSPECTION = "file_inspection"

AI_COMMAND_DISPLAY_A_CUCUMBER = "display_a_cucumber"
AI_COMMAND_DISPLAY_CURRENT_FILES_LIST = "display_current_files_list"
AI_COMMAND_DISPLAY_THE_CURRENT_SOFTWARE_LOGO = "display_the_current_software_logo"
AI_COMMAND_ANSWER_WITH_NATURAL_HUMAN_LANGUAGE = "answer_with_natural_human_language"


class Assistant(BaseClass):
    def __init__(
        self,
        kernel: "Kernel",
        default_model: str
    ) -> None:
        self.kernel = kernel
        self._model: Optional[AbstractModel] = None
        self.models: Dict[str, AbstractModel] = {
            MODEL_NAME_OLLAMA_MISTRAL: OllamaModel(
                self.kernel, MODEL_NAME_OLLAMA_MISTRAL
            ),
            MODEL_NAME_OPEN_AI_GPT_3_5_TURBO: OpenAiModel(
                self.kernel, MODEL_NAME_OPEN_AI_GPT_3_5_TURBO
            ),
            MODEL_NAME_OPEN_AI_GPT_4: OpenAiModel(
                self.kernel, MODEL_NAME_OPEN_AI_GPT_4
            ),
        }

        self.subject_file: Optional[str] = None
        self.set_model(default_model)
        self.completer = WordCompleter([
            "/exit",
            "/menu",
            "/talk_about_file",
            "/?",
        ], pattern=re.compile(r'/\S*'))

        # Create tools
        all_commands = registry_get_all_commands(self.kernel)
        self.tools = []

        self.identities = {
            AI_IDENTITY_DEFAULT: {"system": "You are a helpful AI bot."},
            AI_IDENTITY_CODE_FILE_PATCHER: {
                "system": "You are a helpful AI bot."
                          "\nNow we are talking about this file : {file_full_path}"
                          "\n_______________________________________File metadata"
                          "\nCreation Date: {file_creation_date}"
                          "\nFile Size: {file_size} bytes"
                          "\n_________________________________________End of file info"
            },
            AI_IDENTITY_FILE_INSPECTION: {
                "system": "Answer the question based only on the following context:"
                          "\n"
                          "\n{context}"
            }
        }

        for command_name in all_commands:
            properties = all_commands[command_name]["properties"]

            if "ai_tool" in properties and properties["ai_tool"]:
                self.log(f"Loading tool {command_name}")

                command_tool = CommandTool(
                    kernel=self.kernel,
                    name=command_name,
                    description=all_commands[command_name]["description"],
                )

                self.tools.append(command_tool)

        self.log(f"Loaded {len(self.tools)} tools")
        manager: AppAddonManager = cast(AppAddonManager, self.kernel.addons["app"])

        if manager.is_valid_app():
            self.chroma_path = manager.get_env_dir("ai/embeddings", create=True)
        else:
            self.chroma_path = self.kernel.get_or_create_path("tmp") + "ai/embeddings" + os.sep

        self.log(f"Embedding path is {self.chroma_path}")
        self.chroma = chromadb.PersistentClient(path=self.chroma_path)

    def log(self, message: str) -> None:
        self.kernel.io.log(f"  {message}")

    def set_model(self, identifier: str) -> None:
        self.log(f"Model set to : {identifier}")

        self._model = self.models[identifier]

    def get_model(self, name: Optional[str] = None) -> AbstractModel:
        model = self.models[name] if name else self._model
        self._validate__should_not_be_none(model)
        assert isinstance(model, AbstractModel)

        return model

    def start(self, action: Optional[str] = None) -> None:
        previous_action: Optional[str] = None

        current_model = self.get_model()
        asked_exit = False
        while not asked_exit:
            if not action:
                action = self.chat_choose_action(previous_action)
                previous_action = action

            user_command = None
            if action == CHAT_ACTION_FREE_TALK:
                user_command = self.chat()
            elif action == CHAT_ACTION_FREE_TALK_FILE:
                user_command = self.chat_about_file_from(os.getcwd())
            elif action == CHAT_ACTION_CHANGE_MODEL:
                models = {}
                for model in self.models:
                    models[model] = model

                new_model = prompt_choice_dict(
                    "Choose a new language model:",
                    models,
                    default=current_model.identifier,
                )

                self.set_model(new_model)

            if user_command == "/menu":
                action = None
            elif user_command == "/exit":
                action = CHAT_ACTION_EXIT
            elif user_command == "/talk_about_file":
                action = CHAT_ACTION_FREE_TALK_FILE

            if action == CHAT_ACTION_EXIT:
                asked_exit = True

        self.log(f"{os.linesep}Ciao")

    def chat_about_file_from(self, base_dir: str) -> Optional[str]:
        # Use two dicts to keep dirs and files separated ignoring emojis in alphabetical sorting.
        choices_dirs = {"..": ".."}
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
            if os.path.isfile(full_path):
                return self.chat_about_file(full_path)
            elif os.path.isdir(full_path):
                return self.chat_about_file_from(full_path)

    def chat_about_file(self, full_path: str) -> Optional[str]:
        self.log(f"Chatting about {full_path}")

        self.vector_store_file(full_path)
        self.subject_file = full_path

        return self.chat()

    def vector_delete_file(self, file_path: str):
        collection = self.chroma.get_or_create_collection("single_files")

        # Check for existing documents by the same source, regardless of the signature
        # This is to find any versions of the file, not just ones with a matching signature
        existing_docs = collection.get(
            where={"source": file_path},
        )

        # If there are existing documents, delete them before proceeding
        if len(existing_docs["ids"]) > 0:
            self.log("Existing document versions found. Deleting...")
            collection.delete(ids=existing_docs["ids"])

    def vector_store_file(self, file_path: str):
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_community.document_loaders import TextLoader

        text_splitter = RecursiveCharacterTextSplitter()
        loader = TextLoader(file_path)
        collection = self.chroma.get_or_create_collection("single_files")
        file_signature = file_build_signature(file_path)

        results = collection.get(
            where={"signature": file_signature},
            include=["metadatas"]
        )

        # Delete every version
        self.vector_delete_file(file_path)

        if len(results["ids"]) > 0:
            self.log("Document already exists. Skipping...")
            return

        # If the file is not already in Chroma, proceed with indexing
        self.log("Storing document to vector database...")
        loader.load()
        chunks = loader.load_and_split(text_splitter=text_splitter)

        # Ensuring metadata is correctly attached to each chunk.
        for chunk in chunks:
            chunk.metadata = {'signature': file_signature, "source": file_path}

        # Create a new DB from the documents (or add to existing)
        chroma = Chroma.from_documents(
            chunks,
            self.get_model(MODEL_NAME_OPEN_AI_GPT_4).create_embeddings(),
            collection_name="single_files",
            persist_directory=self.chroma_path
        )
        chroma.persist()
        self.log("Document stored successfully.")

    def chat_choose_action(self, last_action: Optional[str]) -> Optional[str]:
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

        choices[CHAT_ACTION_EXIT] = CHAT_ACTIONS_TRANSLATIONS[CHAT_ACTION_EXIT]

        action = prompt_choice_dict(
            "Choose an action to do with ai assistant:",
            choices,
            abort=None,
            default=CHAT_ACTION_FREE_TALK,
        )

        return str(action) if action else None

    def show_help(self) -> None:
        self.log("Type '/exit' to quit.")
        self.log("Type '/menu' to pick an action.")
        self.log("Type '/?' or '/help' to display this message again.")

    def chat(
        self,
        initial_prompt: Optional[str] = None,
        identity: str = AI_IDENTITY_DEFAULT,
        identity_parameters: Optional[StringKeysDict] = None,
    ) -> str:
        self.show_help()

        while True:
            ai_working = False

            try:
                if not initial_prompt:
                    input = prompt_tool(">>> ", completer=self.completer)
                    user_input_lower = input.strip().lower()

                    if user_input_lower == "exit":
                        user_input_lower = "/exit"

                    if user_input_lower in ["/exit", "/menu", "/talk_about_file"]:
                        return user_input_lower
                else:
                    input = user_input_lower = initial_prompt
                    initial_prompt = None

                if user_input_lower in ["/?", "/help"]:
                    self.show_help()
                else:
                    self.log("..")

                    self.kernel.io.print(COLOR_GRAY, end="")
                    ai_working = True

                    # Talk about a file
                    if self.subject_file:
                        embedding_function = self.get_model(MODEL_NAME_OPEN_AI_GPT_4).create_embeddings()
                        chroma = Chroma(
                            persist_directory=self.chroma_path,
                            embedding_function=embedding_function,
                            collection_name="single_files")

                        results = chroma.similarity_search_with_relevance_scores(
                            input,
                            k=3,
                            filter={'source': self.subject_file})

                        result = self.get_model().request(
                            input,
                            self.identities[AI_IDENTITY_FILE_INSPECTION],
                            identity_parameters or {
                                "context": "\n\n---\n\n".join([doc.page_content for doc, _score in results])
                            }
                        )
                    # Default chatting
                    else:
                        # Enforce model for this task
                        selected_command = self.get_model(MODEL_NAME_OPEN_AI_GPT_4).choose_command(
                            input,
                            [
                                AI_COMMAND_DISPLAY_CURRENT_FILES_LIST,
                                AI_COMMAND_DISPLAY_THE_CURRENT_SOFTWARE_LOGO,
                                AI_COMMAND_DISPLAY_A_CUCUMBER,
                                AI_COMMAND_ANSWER_WITH_NATURAL_HUMAN_LANGUAGE,
                                None,
                            ],
                        )

                        if selected_command == AI_COMMAND_ANSWER_WITH_NATURAL_HUMAN_LANGUAGE:
                            result = self.get_model().request(
                                input,
                                self.identities[identity],
                                identity_parameters or {}
                            )

                        elif selected_command == AI_COMMAND_DISPLAY_A_CUCUMBER:
                            result = "🥒"
                        else:
                            result = f"TODO COMMAND : {selected_command}"

                    # Let a new line separator
                    self.kernel.io.print(COLOR_RESET)
                    self.kernel.io.print(result)
            except KeyboardInterrupt:
                # User asked to quit
                if not ai_working:
                    return "/exit"
                # User asked to interrupt assistant.
                else:
                    self.kernel.io.print(os.linesep)
