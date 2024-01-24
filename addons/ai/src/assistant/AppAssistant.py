import os
from typing import TYPE_CHECKING, Optional

from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from addons.ai.src.assistant.Assistant import Assistant
from src.const.types import StringKeysDict

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


class AppAssistant(Assistant):
    def __init__(self, manager: "AppAddonManager") -> None:
        super().__init__(manager.kernel)

        self.manager = manager

    def assist(self, question: str) -> StringKeysDict:
        prompt = PromptTemplate.from_file(f"{self.manager.kernel.directory.path}addons/ai/samples/prompts/react.txt")

        agent = create_react_agent(
            self.llm,
            self.tools,
            prompt=prompt
        )

        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True)

        return agent_executor.invoke(
            {"input": question}
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
