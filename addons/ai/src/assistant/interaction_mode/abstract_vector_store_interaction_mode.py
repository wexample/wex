from abc import abstractmethod
from typing import Dict, List, Optional, cast, TYPE_CHECKING

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, UnstructuredURLLoader
from langchain_community.document_loaders.parsers.language.language_parser import (
    Language,
)
from langchain_core.documents.base import Document
from langchain_core.vectorstores import VectorStore
from langchain_postgres.vectorstores import PGVector
from unstructured.cleaners.core import clean, clean_extra_whitespace, remove_punctuation
from wexample_helpers.helpers.json import json_load_if_valid
from langchain_community.document_loaders.base import BaseLoader

from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import (
    AbstractInteractionMode,
)
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import AbstractInteractionResponse
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from addons.ai.src.model.open_ai_model import MODEL_NAME_OPEN_AI_GPT_4
from src.helper.file import file_get_extension

if TYPE_CHECKING:
    from addons.ai.src.assistant.assistant import Assistant


class AbstractVectorStoreInteractionMode(AbstractInteractionMode):
    def __init__(self, assistant: "Assistant") -> None:
        super().__init__(assistant)
        self.vectorstore: VectorStore
        self.init_vector_store()

    @abstractmethod
    def get_vector_store_collection_name(self) -> str:
        pass

    @abstractmethod
    def get_storage_signature(self) -> str:
        pass

    def process_user_input(
        self,
        prompt_section: "UserPromptSection",
        remaining_sections: List["UserPromptSection"],
    ) -> AbstractInteractionResponse:

        prompt_section.prompt_configurations.append(
            ("system", "## CONTEXT:" "\n{context}")
        )

        return super().process_user_input(
            prompt_section,
            remaining_sections,
        )

    @abstractmethod
    def get_similarity_search_filter(
        self, prompt_section: UserPromptSection
    ) -> Dict[str, str]:
        pass

    def get_interaction_mode_prompt_parameters(
        self, prompt_section: UserPromptSection
    ) -> Dict[str, str]:
        results = self.vectorstore.similarity_search_with_relevance_scores(
            prompt_section.prompt or "",
            k=3,
            filter=self.get_similarity_search_filter(prompt_section),
        )

        return {
            "context": "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        }

    def init_vector_store(self) -> None:
        self.vectorstore = PGVector(
            embeddings=self.assistant.get_model(
                MODEL_NAME_OPEN_AI_GPT_4
            ).create_embeddings(),
            collection_name=self.get_vector_store_collection_name(),
            connection=self.assistant.database.engine,
            use_jsonb=True,
        )
        self.vectorstore.drop_tables()
        self.vectorstore.create_tables_if_not_exists()
        self.vectorstore.create_collection()

    def vector_create_file_loader(self, file_path: str) -> BaseLoader:
        # Dynamically determine the loader based on file extension
        extension = file_get_extension(file_path)

        if extension == "md":
            self.assistant.log(f"Loader : Markdown")
            from langchain_community.document_loaders import UnstructuredMarkdownLoader

            return cast(BaseLoader, UnstructuredMarkdownLoader(file_path))
        elif extension == "csv":
            self.assistant.log(f"Loader : CSV")
            from langchain_community.document_loaders.csv_loader import CSVLoader

            return cast(BaseLoader, CSVLoader(file_path))
        elif extension == "html":
            self.assistant.log(f"Loader : HTML")
            from langchain_community.document_loaders import UnstructuredHTMLLoader

            return cast(BaseLoader, UnstructuredHTMLLoader(file_path))
        elif extension == "json":
            self.assistant.log(f"Loader : JSON")
            from langchain_community.document_loaders import JSONLoader

            if json_load_if_valid(file_path):
                return cast(
                    BaseLoader,
                    JSONLoader(file_path=file_path, jq_schema=".", text_content=False),
                )
            return cast(BaseLoader, TextLoader(file_path))
        elif extension == "pdf":
            self.assistant.log(f"Loader : PDF")
            from langchain_community.document_loaders import PyPDFLoader

            return cast(BaseLoader, PyPDFLoader(file_path=file_path))
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

                return cast(
                    BaseLoader,
                    GenericLoader.from_filesystem(
                        file_path,
                        parser=LanguageParser(language=language, parser_threshold=1000),
                    ),
                )

            self.assistant.log("Loader : default")

            # Fallback to a generic text loader if file type is not specifically handled
            return cast(BaseLoader, TextLoader(file_path))

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
            from langchain_text_splitters import Language

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

        # If the file is not already in Chroma, proceed with indexing
        self.assistant.log("Storing document to vector database...")
        loader.load()

        chunks = text_splitter.split_documents(loader.load())

        # Ensuring metadata is correctly attached to each chunk.
        for chunk in chunks:
            chunk.metadata = {"signature": file_signature, "source": file_path}

        return chunks

    def vector_store_file(self, file_path: str, signature: str) -> None:
        self.assistant.log(f"Storing document {file_path}")

        chunks = self.vector_create_file_chunks(file_path, signature)

        # Ignore if empty or null, document already stored.
        if len(chunks) == 0:
            return None

        self.vectorstore.add_documents(chunks)

        self.assistant.log("Document stored successfully")

        return None

    def vector_store_url(self, url: str, signature: str) -> None:
        loader = UnstructuredURLLoader(
            urls=[url],
            mode="elements",
            post_processors=[clean, remove_punctuation, clean_extra_whitespace],
        )

        elements = loader.load()
        selected_elements = [
            e for e in elements if e.metadata["category"] == "NarrativeText"
        ]
        full_clean = " ".join([e.page_content for e in selected_elements])

        self.vectorstore.add_documents(
            [Document(page_content=full_clean, metadata={"signature": signature})]
        )
