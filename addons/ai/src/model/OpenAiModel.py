from addons.ai.src.model.DefaultModel import DefaultModel
from langchain_openai import OpenAI

from dotenv import dotenv_values


class OpenAiModel(DefaultModel):
    def __init__(self, kernel: "Kernel", name: str = "open_ai"):
        super().__init__(name, kernel)

        env_path = kernel.directory.path + ".env"
        key = dotenv_values(env_path).get("OPENAI_API_KEY")
        if not key:
            kernel.io.error(
                f"Missing configuration OPENAI_API_KEY in {env_path}"
            )

        self.llm = OpenAI(api_key=key)
