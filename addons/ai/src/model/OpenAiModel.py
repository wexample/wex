from langchain_openai import ChatOpenAI
from dotenv import dotenv_values
from typing import TYPE_CHECKING

from src.const.types import StringKeysDict
from addons.ai.src.model.AbstractModel import AbstractModel

MODEL_NAME_OPEN_AI_GPT_3_5_TURBO_1106 = "open_ai:gpt-3.5-turbo-1106"
MODEL_NAME_OPEN_AI_GPT_3_5_TURBO_16K = "open_ai:gpt-3.5-turbo-16k"
MODEL_NAME_OPEN_AI_GPT_3_5_TURBO = "open_ai:gpt-3.5-turbo"
MODEL_NAME_OPEN_AI_GPT_4 = "open_ai:gpt-4"

if TYPE_CHECKING:
    from langchain_core.language_models import BaseLanguageModel


class OpenAiModel(AbstractModel):
    def activate(self) -> None:
        env_path = self.kernel.directory.path + ".env"
        key = dotenv_values(env_path).get("OPENAI_API_KEY")
        if not key:
            self.kernel.io.error(f"Missing configuration OPENAI_API_KEY in {env_path}")

        self.llm = ChatOpenAI(
            api_key=key,
        )

    def request(
        self,
        input: str,
        identity: StringKeysDict,
        identity_parameters: StringKeysDict) -> "BaseLanguageModel":
        return self.llm(
            self.chat_create_prompt(identity).format_prompt(
                **self.chat_merge_parameters(identity_parameters)
            )
            .to_messages()
        )
