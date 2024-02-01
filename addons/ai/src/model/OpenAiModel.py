from typing import cast, Any

from dotenv import dotenv_values
from langchain_openai import ChatOpenAI

from addons.ai.src.model.AbstractModel import AbstractModel
from src.const.types import StringKeysDict

MODEL_NAME_OPEN_AI_GPT_3_5_TURBO_1106 = "open_ai:gpt-3.5-turbo-1106"
MODEL_NAME_OPEN_AI_GPT_3_5_TURBO_16K = "open_ai:gpt-3.5-turbo-16k"
MODEL_NAME_OPEN_AI_GPT_3_5_TURBO = "open_ai:gpt-3.5-turbo"
MODEL_NAME_OPEN_AI_GPT_4 = "open_ai:gpt-4"


class OpenAiModel(AbstractModel):
    def activate(self) -> None:
        env_path = self.kernel.directory.path + ".env"
        key = dotenv_values(env_path).get("OPENAI_API_KEY")
        if not key:
            self.kernel.io.error(f"Missing configuration OPENAI_API_KEY in {env_path}")

        self.set_llm(ChatOpenAI(
            api_key=key,
        ))

    def request(
        self, input: str, identity: StringKeysDict, identity_parameters: StringKeysDict
    ) -> Any:
        llm = cast(ChatOpenAI, self.get_llm())

        return llm(
            self.chat_create_prompt(identity)
            .format_prompt(**self.chat_merge_parameters(identity_parameters))
            .to_messages()
        )
