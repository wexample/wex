import os
from typing import TYPE_CHECKING, Optional

from dotenv import dotenv_values
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_openai import OpenAI
from langchain_community.tools import Tool, DuckDuckGoSearchResults
from langchain.agents import initialize_agent, AgentType

from src.const.types import StringKeysDict

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


class AppAssistant:
    def __init__(self, manager: "AppAddonManager") -> None:
        self.manager = manager
        self.manager.get_app_dir()

        env_path = manager.kernel.directory.path + ".env"
        key = dotenv_values(env_path).get("OPENAI_API_KEY")
        if not key:
            manager.kernel.io.error(
                f"Missing configuration OPENAI_API_KEY in {env_path}"
            )

        self.llm = OpenAI(api_key=key)

    def create_chain(self, prompt_template: ChatPromptTemplate) -> LLMChain:
        return LLMChain(
            llm=self.llm,
            prompt=prompt_template,
        )

    def assist(self, question: str) -> StringKeysDict:
        def say_hello(input: str) -> str:
            return f"HELLO{input}"

        def say_bye(input: str) -> str:
            return f"BYE{input}"

        def say_thanks(input: str) -> str:
            return f"THANKS{input}"

        def say_patapouf(input: str) -> str:
            return f"PATAPOUF{input}"

        say_hello_tool = Tool.from_function(
            func=say_hello,
            name="SayHelloTool",
            description="Return the hello string"
        )

        say_bye_tool = Tool.from_function(
            func=say_bye,
            name="SayGoodByeTool",
            description="Return the good bye string"
        )

        say_thanks_tool = Tool.from_function(
            func=say_thanks,
            name="SayThankYou",
            description="Return the thank you string"
        )

        say_patapouf_tool = Tool.from_function(
            func=say_patapouf,
            name="SayPatapouf",
            description="Return the patapouf"
        )

        tools = [say_hello_tool, say_thanks_tool, say_bye_tool, say_patapouf_tool]

        agent = initialize_agent(
            tools=tools,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            llm=self.llm,
            verbose=True
        )

        return agent.run(
            f"Tu as la possibilité d'éxetuer une fonction correspondant à l'expression que je vais te passer, et que tu lui donnera en argument. Choisis une seule fonction et exécute là une seule fois. N'anlyse pas la valeur de retour qui peut te sembler étrange, retourne la sans aucun traitement. Voici l'expression : {question}.")

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
