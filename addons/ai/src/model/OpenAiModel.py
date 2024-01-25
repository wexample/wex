from dotenv import dotenv_values
from openai import OpenAI

from addons.ai.src.model.AbstractModel import AbstractModel
from src.const.types import StringKeysDict

MODEL_NAME_OPEN_AI_GPT_3_5_TURBO = "open_ai:gpt-3.5-turbo"
MODEL_NAME_OPEN_AI_GPT_4 = "open_ai:gpt-4"


class OpenAiModel(AbstractModel):
    def activate(self):
        env_path = self.kernel.directory.path + ".env"
        key = dotenv_values(env_path).get("OPENAI_API_KEY")
        if not key:
            self.kernel.io.error(f"Missing configuration OPENAI_API_KEY in {env_path}")

        self.llm = OpenAI(api_key=key)

    def request(
        self,
        question: str,
        identity: StringKeysDict):
        response = self.llm.chat.completions.create(
            model=self.name,
            messages=[
                {"role": "system", "content": identity["system"]},
                {"role": "user", "content": question}
            ]
        )

        return response.choices[0].message.content
