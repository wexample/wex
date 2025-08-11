from typing import List, Optional

from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import (
    AbstractInteractionMode,
)
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import (
    AbstractInteractionResponse,
)
from addons.ai.src.assistant.interaction_response.string_interaction_response import (
    StringInteractionResponse,
)
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from addons.ai.src.tool.command_tool import CommandTool
from src.helper.registry import registry_get_all_commands


class ToolPickerInteractionMode(AbstractInteractionMode):
    tools: List[CommandTool]

    def get_initial_prompt(self, prompt_section: UserPromptSection) -> Optional[str]:
        return (
            "Efficiently answer the questions using one of available tools, "
            "then return the answer after first response:"
            "\n\n{tools}\n\nAdhere to this structure:"
            "\n\nQuestion: the query you need to address"
            "\nThought: consider your approach carefully"
            "\nAction: the chosen action, from [{tool_names}]"
            "\nAction Input: details for the action"
            "\nObservation: outcome of the action"
            "\nConcluding Thought: the insight leading to the final answer"
            "\nFinal Answer: the comprehensive response to the original question"
            "\n\nInitiate with:"
            "\n\nQuestion: {input}"
            "\nThought:{agent_scratchpad}"
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

    def process_user_input(
        self,
        prompt_section: UserPromptSection,
        remaining_sections: List[UserPromptSection],
    ) -> AbstractInteractionResponse:
        self.init_tools()

        if not prompt_section.prompt:
            return StringInteractionResponse("Please ask some question to help agent pick a tool.")

        result = self.assistant.get_model().chat_agent(
            self,
            prompt_section,
            self.tools,
        )
        return StringInteractionResponse(result if result is not None else "")
