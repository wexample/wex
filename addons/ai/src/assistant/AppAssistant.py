import os
from typing import TYPE_CHECKING, Any, Optional, cast

from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain_openai import OpenAI  # type: ignore

from addons.app.command.env.get import app__env__get
from src.const.types import StringKeysDict

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


class AppAssistant:
    def __init__(self, manager: "AppAddonManager") -> None:
        self.manager = manager
        app_dir = self.manager.get_app_dir()

        key = manager.kernel.run_function(
            app__env__get, {"app-dir": app_dir, "key": "OPENAI_API_KEY"}
        ).first()

        self.llm = OpenAI(openai_api_key=key)

    def create_chain(self, prompt_template: ChatPromptTemplate) -> LLMChain:
        return LLMChain(
            llm=self.llm,
            prompt=prompt_template,
        )

    def assist(self, question: str) -> StringKeysDict:
        human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")

        chain = self.create_chain(
            ChatPromptTemplate.from_messages([human_message_prompt])
        )

        return chain.invoke(cast(Any, question))

    def load_file(self, file_path: str) -> Optional[str]:
        if not os.path.exists(file_path):
            return None

        with open(file_path, "r") as f:
            return f.read()

    def load_example_patch(self, name: str) -> StringKeysDict:
        base_path = f"{self.manager.get_app_dir()}.wex/command/samples/examples/{name}/"

        return {
            "prompt": self.load_file(f"{base_path}prompt.txt"),
            "source": self.load_file(f"{base_path}source.py"),
            "patch": self.load_file(f"{base_path}response.patch"),
            "tree": self.load_file(f"{base_path}tree.yml"),
        }
