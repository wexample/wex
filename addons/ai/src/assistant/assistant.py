import os
from typing import TYPE_CHECKING, Dict, List, Optional, cast

import chromadb  # type: ignore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders.parsers.language.language_parser import (
    Language,
)  # type: ignore
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.document_loaders import BaseLoader  # type: ignore
from langchain_core.documents.base import Document
from prompt_toolkit import HTML, print_formatted_text

from addons.ai.src.assistant.prompt_manager import PromptManager
from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from addons.ai.src.assistant.subject.default_chat_subject import DefaultSubject
from addons.ai.src.assistant.subject.file_chat_subject import FileChatSubject
from addons.ai.src.assistant.subject.help_chat_subject import HelpChatSubject
from addons.ai.src.assistant.subject.investigate_chat_subject import InvestigateChatSubject
from addons.ai.src.assistant.subject.tool_chat_subject import ToolChatSubject
from addons.ai.src.assistant.utils.globals import (
    AI_IDENTITY_CODE_FILE_PATCHER,
    AI_IDENTITY_COMMAND_SELECTOR,
    AI_IDENTITY_DEFAULT,
    AI_IDENTITY_FILE_INSPECTION,
    AI_IDENTITY_GIT_PATCH_CREATOR,
    AI_IDENTITY_TOOLS_AGENT,
    ASSISTANT_DEFAULT_COMMANDS,
    CHAT_MENU_ACTION_CHAT,
    CHAT_MENU_ACTION_CHANGE_DEFAULT_MODEL,
    CHAT_MENU_ACTION_THEME,
    CHAT_MENU_ACTION_EXIT,
    CHAT_MENU_ACTIONS_TRANSLATIONS,
    AI_FUNCTION_DISPLAY_A_CUCUMBER,
    AI_COMMAND_PREFIX,
    AI_IDENTITY_INVESTIGATOR,
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
from src.const.types import StringKeysDict
from src.core.KernelChild import KernelChild
from src.core.spinner import Spinner
from src.helper.data_json import load_json_if_valid
from src.helper.file import file_build_signature, file_get_extension
from src.helper.prompt import prompt_choice_dict, prompt_progress_steps

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class Assistant(KernelChild):
    subject: Optional[AbstractChatSubject] = None
    _default_model: Optional[AbstractModel] = None

    def __init__(self, kernel: "Kernel", default_model: str) -> None:
        super().__init__(kernel)

        self._initial_default_model = default_model
        self.colors_theme: Optional[str] = None

        prompt_progress_steps(
            kernel,
            [
                self._init_models,
                self._init_vector_database,
                self._init_prompt,
                self._init_commands,
                self._init_identities,
                self._init_subjects,
            ],
        )

    def _init_models(self) -> None:
        self._default_model: Optional[AbstractModel] = None
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

        self.set_default_model(self._initial_default_model)

    def _init_prompt(self) -> None:
        self.prompt_manager = PromptManager(self)
        self.spinner = Spinner()

    def _init_commands(self) -> None:
        self.commands = ASSISTANT_DEFAULT_COMMANDS

    def _init_subjects(self) -> None:
        subjects = [
            FileChatSubject,
            HelpChatSubject,
            ToolChatSubject,
            InvestigateChatSubject,
            # Should be last, as fallback
            DefaultSubject,
        ]

        self.subjects: Dict[str, AbstractChatSubject] = {}
        for subject_class in subjects:
            subject = cast(AbstractChatSubject, subject_class(self))
            self.subjects[subject.name()] = subject

    def _init_identities(self) -> None:
        self.identities = {
            AI_IDENTITY_DEFAULT: {"system": "You are a supportive AI assistant."},
            AI_IDENTITY_CODE_FILE_PATCHER: {
                "system": "You are a supportive AI assistant."
                          "\nFocused on this file: {file_full_path}"
                          "\n_______________________________________File metadata"
                          "\nCreation Date: {file_creation_date}"
                          "\nFile Size: {file_size} bytes"
                          "\n_______________________________________End of file metadata"
            },
            AI_IDENTITY_COMMAND_SELECTOR: {
                "system": "Provide a command name that aids in responding to the user's query, or None if not applicable."
            },
            AI_IDENTITY_FILE_INSPECTION: {
                "system": "Respond to inquiries based solely on the provided context:"
                          "\n"
                          "\n{context}"
            },
            AI_IDENTITY_GIT_PATCH_CREATOR: {
                "system": "You generate file diffs in unidiff format based on user instructions, and wrapped into a json object."
                          "\nStart the patch with \"# PATCH_START\" then the patch content without header."
                          "\nThe patch body always starts 3 lines before the first change, if applicable, this is the security margin."
                          "\nYou respect the exact original spacings, indentation."
                          "\nYou do not do any change without marking it with a + or a -."
                          "\nTerminate with the # DESCRIPTION: information describing what you've done."
            },
            AI_IDENTITY_TOOLS_AGENT: {
                "system": "Efficiently answer the questions using one of available tools, then return the answer after first response:"
                          "\n\n{tools}\n\nAdhere to this structure:"
                          "\n\nQuestion: the query you need to address"
                          "\nThought: consider your approach carefully"
                          "\nAction: the chosen action, from [{tool_names}]"
                          "\nAction Input: details for the action"
                          "\nObservation: outcome of the action"
                          "\nConcluding Thought: the insight leading to the final answer"
                          "\nFinal Answer: the comprehensive response to the original question"
                          "\n\nInitiate with:"
                          "\n\nQuestion: {input}"
                          "\nThought:{agent_scratchpad}"
            },
            AI_IDENTITY_INVESTIGATOR: {
                "system": "You will ask the user questions so that we can identify the source of the problem together."
                          "Start with only the first question. Be as concise as possible, "
                          "no unnecessary introductions or explanations. "
                          "The user will provide what they find, "
                          "and then you will ask the next question based on that result."
            }
        }

    def _init_vector_database(self) -> None:
        manager: AppAddonManager = cast(AppAddonManager, self.kernel.addons["app"])

        if manager.is_valid_app():
            self.chroma_path = manager.get_env_dir("ai/embeddings", create=True)
        else:
            self.chroma_path = (
                self.kernel.get_or_create_path("tmp") + "ai/embeddings" + os.sep
            )

        self.log(f"Embedding path is {self.chroma_path}")
        self.chroma = chromadb.PersistentClient(path=self.chroma_path)

    def set_default_subject(self) -> None:
        self.set_subject(DefaultSubject.name())

    def set_subject(self, name: str) -> AbstractChatSubject:
        subject = cast(AbstractChatSubject, self.subjects[name])

        self.log("Setting subject : " + subject.introduce())
        self.subject = subject

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

    def get_default_model(self, name: Optional[str] = None) -> AbstractModel:
        model = self.models[name] if name else self._default_model
        self._validate__should_not_be_none(model)
        assert isinstance(model, AbstractModel)

        return model

    def start(self, menu_action: Optional[str] = None) -> None:
        asked_exit = False
        while not asked_exit:
            if not menu_action:
                menu_action = self.show_menu()

            if menu_action == CHAT_MENU_ACTION_CHAT:
                self.set_default_subject()
                menu_action = self.chat()
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
            elif menu_action == CHAT_MENU_ACTION_CHANGE_DEFAULT_MODEL:
                current_model = self.get_default_model()
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

    def vector_delete_file(self, file_path: str) -> None:
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

    def vector_create_file_loader(self, file_path: str) -> BaseLoader:
        # Dynamically determine the loader based on file extension
        extension = file_get_extension(file_path)

        if extension == "md":
            self.log(f"Loader : Markdown")
            from langchain_community.document_loaders import UnstructuredMarkdownLoader

            return UnstructuredMarkdownLoader(file_path)
        elif extension == "csv":
            self.log(f"Loader : CSV")
            from langchain_community.document_loaders.csv_loader import CSVLoader

            return CSVLoader(file_path)
        elif extension == "html":
            self.log(f"Loader : HTML")
            from langchain_community.document_loaders import UnstructuredHTMLLoader

            return UnstructuredHTMLLoader(file_path)
        elif extension == "json":
            self.log(f"Loader : JSON")
            from langchain_community.document_loaders import JSONLoader

            if load_json_if_valid(file_path):
                return JSONLoader(file_path=file_path, jq_schema=".", text_content=False)
            return TextLoader(file_path)
        elif extension == "pdf":
            self.log(f"Loader : PDF")
            from langchain_community.document_loaders import PyPDFLoader

            return PyPDFLoader(file_path=file_path)
        else:
            language = self.vector_find_language_by_extension(
                file_get_extension(file_path)
            )

            if language:
                from langchain_community.document_loaders.generic import GenericLoader
                from langchain_community.document_loaders.parsers.language import (
                    LanguageParser,
                )

                self.log(f"Loader : {language}")

                return GenericLoader.from_filesystem(
                    file_path,
                    parser=LanguageParser(language=language, parser_threshold=1000),
                )

            self.log("Loader : default")

            # Fallback to a generic text loader if file type is not specifically handled
            return TextLoader(file_path)

    def vector_find_language_by_extension(self, extension: str) -> Optional[Language]:
        # @from https://python.langchain.com/docs/integrations/document_loaders/source_code/
        extensions_map = {
            "c": ["c"],  # C (*)
            "cpp": ["cpp", "h", "hpp"],  # C++ (*)
            "csharp": ["cs"],  # C# (*)
            "cobol": ["cob", "cpy"],  # COBOL
            "go": ["go"],  # Go (*)
            "java": ["java"],  # Java (*)
            "js": ["js"],  # JavaScript (*) requires package esprima
            "kotlin": ["kt"],  # Kotlin (*)
            "lua": ["lua"],  # Lua (*)
            "perl": ["pl"],  # Perl (*)
            "python": ["py"],  # Python
            "ruby": ["rb"],  # Ruby (*)
            "rust": ["rs"],  # Rust (*)
            "scala": ["scala"],  # Scala (*)
            "typescript": ["ts"],  # TypeScript (*)
        }

        for language, extensions in extensions_map.items():
            if extension in extensions:
                return cast(Language, language)

        return None

    def vector_create_text_splitter(
        self, file_path: str
    ) -> RecursiveCharacterTextSplitter:
        language = self.vector_find_language_by_extension(file_get_extension(file_path))

        if language:
            self.log(f"Splitter : {language}")
            from langchain_text_splitters import Language  # type: ignore

            return RecursiveCharacterTextSplitter.from_language(
                language=cast(Language, language), chunk_size=50, chunk_overlap=0
            )
        else:
            self.log(f"Splitter : default")
            return RecursiveCharacterTextSplitter()

    def vector_create_file_chunks(
        self, file_path: str, file_signature: str
    ) -> List[Document]:
        loader = self.vector_create_file_loader(file_path)
        text_splitter = self.vector_create_text_splitter(file_path)
        collection = self.chroma.get_or_create_collection("single_files")

        results = collection.get(
            where={"signature": file_signature}, include=["metadatas"]
        )

        if len(results["ids"]) > 0:
            self.log("Document already exists. Skipping...")
            return []

        # Delete every version
        self.vector_delete_file(file_path)

        # If the file is not already in Chroma, proceed with indexing
        self.log("Storing document to vector database...")
        loader.load()

        chunks = cast(List[Document], text_splitter.split_documents(loader.load()))

        # Ensuring metadata is correctly attached to each chunk.
        for chunk in chunks:
            chunk.metadata = {"signature": file_signature, "source": file_path}

        return chunks

    def vector_store_file(self, file_path: str) -> None:
        file_signature = file_build_signature(file_path)
        chunks = self.vector_create_file_chunks(file_path, file_signature)

        # Ignore if empty or null, document already stored.
        if len(chunks) == 0:
            return None

        # Create a new DB from the documents (or add to existing)
        chroma = Chroma.from_documents(
            chunks,
            self.get_default_model(MODEL_NAME_OPEN_AI_GPT_4).create_embeddings(),
            collection_name="single_files",
            persist_directory=self.chroma_path,
        )
        chroma.persist()
        self.log("Document stored successfully.")

        return None

    def show_menu(self) -> Optional[str]:
        choices = {
            CHAT_MENU_ACTION_CHAT: CHAT_MENU_ACTIONS_TRANSLATIONS[CHAT_MENU_ACTION_CHAT],
        }

        if len(self.models.keys()) > 1:
            choices[CHAT_MENU_ACTION_CHANGE_DEFAULT_MODEL] = CHAT_MENU_ACTIONS_TRANSLATIONS[
                CHAT_MENU_ACTION_CHANGE_DEFAULT_MODEL
            ]

        choices[CHAT_MENU_ACTION_THEME] = CHAT_MENU_ACTIONS_TRANSLATIONS[CHAT_MENU_ACTION_THEME]
        choices[CHAT_MENU_ACTION_EXIT] = CHAT_MENU_ACTIONS_TRANSLATIONS[CHAT_MENU_ACTION_EXIT]

        action = prompt_choice_dict(
            "Choose an action to do with ai assistant:",
            choices,
            abort=None,
            default=CHAT_MENU_ACTION_CHAT,
        )

        return str(action) if action else None

    def guess_function(self, user_input: str) -> Optional[str]:
        selected_function = self.get_default_model(MODEL_NAME_OPEN_AI_GPT_4).guess_function(
            user_input,
            [
                AI_FUNCTION_DISPLAY_A_CUCUMBER,
                None,
            ],
            self.identities[AI_IDENTITY_COMMAND_SELECTOR],
        )

        # Demo usage
        if selected_function == AI_FUNCTION_DISPLAY_A_CUCUMBER:
            return "🥒"

        return None

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
        identity_name: str = AI_IDENTITY_DEFAULT,
        identity_parameters: Optional[StringKeysDict] = None,
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

                    if command == "exit":
                        return CHAT_MENU_ACTION_EXIT
                    elif command == "menu":
                        return None
                    elif command == "function":
                        result = self.guess_function(prompt_section.prompt)
                    else:
                        # Loop on subjects until one returns something.
                        for subject in self.subjects.values():
                            # Accepts "bool" return to block process without returning message.
                            if command in subject.get_completer_commands():
                                result = cast(AbstractChatSubject, subject).process_user_input(
                                    prompt_section,
                                    self.identities[identity_name],
                                    identity_parameters or {},
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
