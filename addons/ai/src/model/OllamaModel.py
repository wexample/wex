from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from src.const.globals import VERBOSITY_LEVEL_MAXIMUM

from addons.ai.src.model.AbstractModel import AbstractModel
from src.const.types import StringKeysDict

MODEL_NAME_OLLAMA_MISTRAL = "ollama:mistral"


class OllamaModel(AbstractModel):
    def activate(self):
        # We should start ollama container

        self.llm = Ollama(
            model=self.name,
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        )

    def request(
        self,
        input: str,
        identity: StringKeysDict,
        identity_parameters: StringKeysDict):
        self.kernel.io.log(identity["system"], verbosity=VERBOSITY_LEVEL_MAXIMUM)
        self.kernel.io.log(identity_parameters, verbosity=VERBOSITY_LEVEL_MAXIMUM)

        chain = LLMChain(
            llm=self.llm,
            prompt=self.chat_create_prompt(identity),
            verbose=False
        )

        return chain.invoke(
            self.chat_merge_parameters(identity_parameters)
        )["text"].strip()
