from typing import Optional, List

from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from addons.ai.src.assistant.utils.globals import AI_IDENTITY_TOOLS_AGENT
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from addons.ai.src.tool.command_tool import CommandTool
from src.const.types import StringKeysDict
from src.helper.registry import registry_get_all_commands

SUBJECT_TOOL_CHAT_COMMAND_AGENT = "agent"


class AgentChatSubject(AbstractChatSubject):
    tools: List[CommandTool]

    @staticmethod
    def name() -> str:
        return "tool"

    def introduce(self) -> str:
        return f"Ask agent to use a tool (beta)"

    def get_completer_commands(self) -> StringKeysDict:
        return {
            SUBJECT_TOOL_CHAT_COMMAND_AGENT: "Use tool",
        }

    def process_user_input(
        self,
        prompt_section: UserPromptSection,
        identity: StringKeysDict,
        identity_parameters: StringKeysDict,
        remaining_sections: List[UserPromptSection]
    ) -> Optional[bool | str]:
        self.init_tools()

        if not prompt_section.prompt:
            return "Please ask some question to help agent pick a tool."

        return self.assistant.get_model().chat_agent(
            prompt_section.prompt,
            self.tools,
            self.assistant.identities[AI_IDENTITY_TOOLS_AGENT],
        )

    def init_tools(self) -> None:
        # Create tools
        all_commands = registry_get_all_commands(self.kernel)
        self.tools: List[CommandTool] = []

        for command_name in all_commands:
            properties = all_commands[command_name]["properties"]

            if "ai_tool" in properties and properties["ai_tool"]:
                self.assistant.log(f"Loading tool {command_name}")

                command_tool = CommandTool(
                    kernel=self.kernel,
                    name=command_name,
                    description=all_commands[command_name]["description"],
                )

                self.tools.append(command_tool)

        self.assistant.log(f"Loaded {len(self.tools)} tools")
