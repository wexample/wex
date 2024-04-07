from typing import Optional, TYPE_CHECKING

from langchain_community.vectorstores.chroma import Chroma

from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from addons.ai.src.model.open_ai_model import MODEL_NAME_OPEN_AI_GPT_4
from addons.ai.src.assistant.utils.identities import AI_IDENTITY_FILE_INSPECTION
from src.const.types import StringKeysDict

if TYPE_CHECKING:
    from addons.ai.src.assistant.assistant import Assistant

SUBJECT_FILE_CHAT_PATCH = 'patch'


class FileChatSubject(AbstractChatSubject):
    def name(self) -> str:
        return "file"

    def introduce(self) -> str:
        return f"Chatting about file {self.get_path()}"

    def __init__(self, assistant: "Assistant", file_path: str) -> None:
        super().__init__(assistant)
        self.file_path = file_path

    def get_path(self) -> str:
        self._validate__should_not_be_none(self.file_path)

        return self.file_path

    def process_user_input(
        self,
        user_input_split: StringKeysDict,
        identity: StringKeysDict,
        identity_parameters: StringKeysDict
    ) -> Optional[str]:
        embedding_function = self.assistant.get_model(
            MODEL_NAME_OPEN_AI_GPT_4
        ).create_embeddings()
        chroma = Chroma(
            persist_directory=self.assistant.chroma_path,
            embedding_function=embedding_function,
            collection_name="single_files",
        )

        user_input = user_input_split["input"]
        results = chroma.similarity_search_with_relevance_scores(
            user_input, k=3, filter={"source": self.get_path()}
        )

        return self.assistant.get_model().chat(
            user_input,
            self.assistant.identities[AI_IDENTITY_FILE_INSPECTION],
            identity_parameters
            or {
                "context": "\n\n---\n\n".join(
                    [doc.page_content for doc, _score in results]
                )
            },
        )
