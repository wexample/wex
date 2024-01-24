import os
from typing import TYPE_CHECKING, Optional

from dotenv import dotenv_values
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_openai import OpenAI
from langchain_community.tools import Tool, DuckDuckGoSearchResults
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import BaseTool, StructuredTool, tool

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
        @tool
        def say_age(name: str) -> str:
            """Return the age of given character"""
            return f"{name} is 840 years"

        say_age_tool = Tool.from_function(
            func=say_age,
            name="Returns the age of given character",
            description="Returns the age of given character"
        )

        @tool
        def say_gender(name: str) -> str:
            """Return the age of given character"""
            return f"{name} has no gender as it comes from the ZOBIZOBI planet which is in another dimension and space time"

        say_gender_tool = Tool.from_function(
            func=say_gender,
            name="Returns the gender of given character",
            description="Returns the gender of given character"
        )

        tools = [say_age_tool, say_gender_tool]
        prompt = hub.pull("hwchase17/react")
        agent = create_react_agent(self.llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        return agent_executor.invoke(
            {"input": f"What is the {question} of XAXOXO"}
        )["output"]

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
