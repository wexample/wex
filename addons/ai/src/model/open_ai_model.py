from typing import Any, List, Optional

from dotenv import dotenv_values
from langchain.chains import create_tagging_chain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from addons.ai.src.model.abstract_model import AbstractModel
from src.const.types import StringKeysDict

MODEL_NAME_OPEN_AI_GPT_3_5_TURBO_1106 = "open_ai:gpt-3.5-turbo-1106"
MODEL_NAME_OPEN_AI_GPT_3_5_TURBO_16K = "open_ai:gpt-3.5-turbo-16k"
MODEL_NAME_OPEN_AI_GPT_3_5_TURBO = "open_ai:gpt-3.5-turbo"
MODEL_NAME_OPEN_AI_GPT_4 = "open_ai:gpt-4"


class OpenAiModel(AbstractModel):
    def activate(self) -> None:
        env_path = self.kernel.directory.path + ".env"
        self.api_key: Optional[str] = dotenv_values(env_path).get("OPENAI_API_KEY")
        if not self.api_key:
            self.kernel.io.error(f"Missing configuration OPENAI_API_KEY in {env_path}")

        self.set_llm(ChatOpenAI(api_key=self.api_key, model_name=self.name))  # type: ignore

    def choose_command(
        self,
        input: str,
        commands: List[str | None],
        identity: StringKeysDict,
    ) -> Optional[str]:
        """
        The tagging mechanism works well on GPT4 only.
        """
        chain = create_tagging_chain(
            {
                "properties": {
                    "command": {
                        "type": "string",
                        "enum": commands,
                        "description": identity["system"],
                    },
                },
            },
            self.get_llm(),
        )

        response = chain.invoke({"input": input})

        return (
            response["text"]["command"]
            if "text" in response and response["text"]["command"] != "None"
            else None
        )

    def create_embeddings(self) -> Any:
        return OpenAIEmbeddings(openai_api_key=self.api_key)  # type: ignore
