from typing import Any, List, Optional

from langchain.chains import create_tagging_chain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import (
    AbstractInteractionMode,
)
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from addons.ai.src.model.abstract_model import AbstractModel

MODEL_NAME_OPEN_AI_GPT_3_5_TURBO_1106 = "open_ai:gpt-3.5-turbo-1106"
MODEL_NAME_OPEN_AI_GPT_3_5_TURBO_16K = "open_ai:gpt-3.5-turbo-16k"
MODEL_NAME_OPEN_AI_GPT_3_5_TURBO = "open_ai:gpt-3.5-turbo"
MODEL_NAME_OPEN_AI_GPT_4 = "open_ai:gpt-4"


class OpenAiModel(AbstractModel):
    api_key: Optional[str] = None

    def activate(self) -> None:
        api_key_val = self.kernel.env("OPENAI_API_KEY", required=True)
        self.api_key = str(api_key_val)

        self.set_llm(ChatOpenAI(api_key=self.api_key, model_name=self.name))  # type: ignore

    def guess_function(
        self,
        interaction_mode: AbstractInteractionMode,
        prompt_section: UserPromptSection,
        functions: List[str | None],
    ) -> Optional[str]:
        """
        The tagging mechanism works well on GPT4 only.
        """
        chain = create_tagging_chain(
            {
                "properties": {
                    "command": {
                        "type": "string",
                        "enum": functions,
                        "description": interaction_mode.get_initial_prompt(
                            prompt_section
                        ),
                    },
                },
            },
            self.get_llm(),
        )

        response = chain.invoke({"input": prompt_section.prompt})

        return (
            response["text"]["command"]
            if "text" in response and response["text"]["command"] != "None"
            else None
        )

    def create_embeddings(self) -> Any:
        return OpenAIEmbeddings(openai_api_key=self.api_key)  # type: ignore
