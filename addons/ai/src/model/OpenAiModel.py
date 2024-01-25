from addons.ai.src.model.DefaultModel import DefaultModel
from langchain_openai import OpenAI
from typing import TYPE_CHECKING

from dotenv import dotenv_values

if TYPE_CHECKING:
    from src.core.Kernel import Kernel

MODEL_NAME_OPEN_AI = "open_ai"

class OpenAiModel(DefaultModel):
    def __init__(self, kernel: "Kernel", name: str = MODEL_NAME_OPEN_AI):
        super().__init__(kernel, name)

    def activate(self):
        env_path = self.kernel.directory.path + ".env"
        key = dotenv_values(env_path).get("OPENAI_API_KEY")
        if not key:
            self.kernel.io.error(
                f"Missing configuration OPENAI_API_KEY in {env_path}"
            )

        self.llm = OpenAI(api_key=key)
