from typing import Any

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain_community.llms import Ollama

from addons.ai.src.model.AbstractModel import AbstractModel
from addons.app.command.app.exec import app__app__exec
from addons.app.command.helper.start import app__helper__start
from addons.app.const.app import HELPER_APP_AI_SHORT_NAME
from src.const.globals import VERBOSITY_LEVEL_MAXIMUM
from src.const.types import StringKeysDict

MODEL_NAME_OLLAMA_MISTRAL = "ollama:mistral"


class OllamaModel(AbstractModel):
    def activate(self) -> None:
        # Start AI helper app
        response = self.kernel.run_function(
            app__helper__start,
            {
                "name": HELPER_APP_AI_SHORT_NAME,
            },
            # Disable async execution
            fast_mode=True,
        )

        app_dir = str(response.last())

        # Start Ollama in helper app
        self.kernel.run_function(
            app__app__exec,
            {"app-dir": app_dir, "command": f"ollama run {self.name}"},
            # Disable async execution
            fast_mode=True,
        )

        # Connect Ollama
        self.set_llm(
            Ollama(
                model=self.name,
                callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
            )
        )

    def request(
        self, input: str, identity: StringKeysDict, identity_parameters: StringKeysDict
    ) -> Any:
        self.kernel.io.log(identity["system"], verbosity=VERBOSITY_LEVEL_MAXIMUM)
        self.kernel.io.log(identity_parameters, verbosity=VERBOSITY_LEVEL_MAXIMUM)

        chain = LLMChain(
            llm=self.get_llm(), prompt=self.chat_create_prompt(identity), verbose=False
        )

        return chain.invoke(self.chat_merge_parameters(identity_parameters))[
            "text"
        ].strip()
