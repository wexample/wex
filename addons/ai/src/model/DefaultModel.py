from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama

from addons.ai.src.model.AbstractModel import AbstractModel

MODEL_NAME_MISTRAL = "mistral"


class DefaultModel(AbstractModel):
    def activate(self):
        # We should start ollama container

        self.llm = Ollama(
            model=self.name,
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        )
