from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from src.const.globals import CORE_COMMAND_NAME

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
        question: str,
        identity: StringKeysDict):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", identity["system"]),
                ("human", "{user_input}"),
            ]
        )

        chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
        )

        return chain.invoke({
            "name": CORE_COMMAND_NAME,
            "user_input": question})["text"].strip()
