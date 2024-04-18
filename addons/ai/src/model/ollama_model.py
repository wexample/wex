from typing import List, Optional, Any

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.llms import Ollama

from addons.ai.src.model.abstract_model import AbstractModel
from addons.app.command.app.exec import app__app__exec
from src.const.types import StringKeysDict

MODEL_NAME_OLLAMA_MISTRAL = "ollama:mistral"


class OllamaModel(AbstractModel):
    def activate(self) -> None:
        # Start Ollama in helper app
        self.kernel.run_function(
            app__app__exec,
            {
                "app-dir": self.assistant.helper_app_dir,
                "command": f"ollama run {self.name}"},
        )

        # Connect Ollama
        self.set_llm(
            Ollama(
                model=self.name,
                callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
            )
        )

    def guess_function(
        self,
        user_input: str,
        functions: List[str | None],
    ) -> Optional[str]:
        self.kernel.io.warn("Guessing function with tagging chain is not supported yet by OllamaModel")
        # Ollama tagging not set up.
        return None

    def create_embeddings(self) -> Any:
        return OllamaEmbeddings()
