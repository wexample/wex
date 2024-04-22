from typing import Optional, List, cast, TYPE_CHECKING

from chromadb import ClientAPI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders.parsers.language.language_parser import (
    Language,
)  # type: ignore
from langchain_core.document_loaders import BaseLoader  # type: ignore
from langchain_core.documents.base import Document
from langchain_postgres.vectorstores import PGVector

from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import AbstractInteractionMode
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from addons.ai.src.model.open_ai_model import MODEL_NAME_OPEN_AI_GPT_4
from src.helper.data_json import json_load_if_valid
from src.helper.file import file_build_signature, file_get_extension

if TYPE_CHECKING:
    from ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject


class FileExploreInteractionMode(AbstractInteractionMode):
    chroma: Optional[ClientAPI] = None
    chroma_path: Optional[str] = None

    def __init__(self, subject: "AbstractChatSubject"):
        super().__init__(subject)

        self.vectorstore = PGVector(
            embeddings=self.assistant.get_model(MODEL_NAME_OPEN_AI_GPT_4).create_embeddings(),
            collection_name="single_files",
            connection=self.assistant.db_engine,
            use_jsonb=True,
        )
        self.vectorstore.drop_tables()
        self.vectorstore.create_tables_if_not_exists()
        self.vectorstore.create_collection()

    @staticmethod
    def name() -> str:
        return "file_explore"

    def get_initial_prompt(self) -> Optional[str]:
        return ("## CONTEXT:"
                "\n{context}")

    def process_user_input(
        self,
        prompt_section: UserPromptSection,
        remaining_sections: List[UserPromptSection]
    ) -> Optional[bool | str]:
        from addons.ai.src.assistant.subject.file_chat_subject import FileChatSubject
        subject = cast(FileChatSubject, self.assistant.get_current_subject())

        # Avoid empty input error.
        if not subject.file_path:
            return f'No file selected'

        self.vector_store_file(subject.file_path)

        # Avoid empty input error.
        if not prompt_section.prompt:
            return f'Please ask something about the file {subject.file_path}'

        results = self.vectorstore.similarity_search_with_relevance_scores(
            prompt_section.prompt,
            k=3,
            filter={
                "source": subject.file_path
            }
        )

        self.assistant.spinner.start()

        response = self.assistant.get_model().chat(
            prompt_section,
            {
                "context": "\n\n---\n\n".join(
                    [doc.page_content for doc, _score in results]
                )
            },
        )

        self.assistant.spinner.stop()

        return response

    def vector_create_file_loader(self, file_path: str) -> BaseLoader:
        # Dynamically determine the loader based on file extension
        extension = file_get_extension(file_path)

        if extension == "md":
            self.assistant.log(f"Loader : Markdown")
            from langchain_community.document_loaders import UnstructuredMarkdownLoader

            return UnstructuredMarkdownLoader(file_path)
        elif extension == "csv":
            self.assistant.log(f"Loader : CSV")
            from langchain_community.document_loaders.csv_loader import CSVLoader

            return CSVLoader(file_path)
        elif extension == "html":
            self.assistant.log(f"Loader : HTML")
            from langchain_community.document_loaders import UnstructuredHTMLLoader

            return UnstructuredHTMLLoader(file_path)
        elif extension == "json":
            self.assistant.log(f"Loader : JSON")
            from langchain_community.document_loaders import JSONLoader

            if json_load_if_valid(file_path):
                return JSONLoader(file_path=file_path, jq_schema=".", text_content=False)
            return TextLoader(file_path)
        elif extension == "pdf":
            self.assistant.log(f"Loader : PDF")
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

                self.assistant.log(f"Loader : {language}")

                return GenericLoader.from_filesystem(
                    file_path,
                    parser=LanguageParser(language=language, parser_threshold=1000),
                )

            self.assistant.log("Loader : default")

            # Fallback to a generic text loader if file type is not specifically handled
            return TextLoader(file_path)

    def vector_delete_file(self, file_path: str) -> None:
        collection = self.chroma.get_or_create_collection("single_files")

        # Check for existing documents by the same source, regardless of the signature
        # This is to find any versions of the file, not just ones with a matching signature
        existing_docs = collection.get(
            where={"source": file_path},
        )

        # If there are existing documents, delete them before proceeding
        if len(existing_docs["ids"]) > 0:
            self.assistant.log("Existing document versions found. Deleting...")
            collection.delete(ids=existing_docs["ids"])

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
            self.assistant.log(f"Splitter : {language}")
            from langchain_text_splitters import Language  # type: ignore

            return RecursiveCharacterTextSplitter.from_language(
                language=cast(Language, language), chunk_size=50, chunk_overlap=0
            )
        else:
            self.assistant.log(f"Splitter : default")
            return RecursiveCharacterTextSplitter()

    def vector_create_file_chunks(
        self, file_path: str, file_signature: str
    ) -> List[Document]:
        loader = self.vector_create_file_loader(file_path)
        text_splitter = self.vector_create_text_splitter(file_path)

        # collection = self.vectorstore.get_collection()

        # results = collection.get(
        #     where={"signature": file_signature}, include=["metadatas"]
        # )
        #
        # if len(results["ids"]) > 0:
        #     self.assistant.log("Document already exists. Skipping...")
        #     return []

        # # Delete every version
        # self.vector_delete_file(file_path)

        # If the file is not already in Chroma, proceed with indexing
        self.assistant.log("Storing document to vector database...")
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

        self.vectorstore.add_documents(
            chunks
        )

        self.assistant.log("Document stored successfully.")

        return None
