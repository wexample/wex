from typing import List, Optional

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama

from addons.ai.src.model.abstract_model import AbstractModel
from addons.app.command.app.exec import app__app__exec
from addons.app.command.helper.start import app__helper__start
from addons.app.const.app import HELPER_APP_AI_SHORT_NAME
from src.const.types import StringKeysDict

MODEL_NAME_OLLAMA_MISTRAL = "ollama:mistral"


class OllamaModel(AbstractModel):
    def activate(self) -> None:
        # Start AI helper app
        response = self.kernel.run_function(
            app__helper__start,
            {
                "name": HELPER_APP_AI_SHORT_NAME,
                "create-network": False,
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

    def choose_command(
        self,
        user_input: str,
        commands: List[str | None],
        identity: StringKeysDict,
    ) -> Optional[str]:
        # Ollama tagging not set up.
        return None
