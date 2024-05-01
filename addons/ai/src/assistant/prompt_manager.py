import html
from typing import TYPE_CHECKING, Any, Dict, Iterable

from prompt_toolkit import HTML
from prompt_toolkit.completion import CompleteEvent, Completer, Completion
from prompt_toolkit.document import Document as ToolkitDocument
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.styles import style_from_pygments_cls
from pygments.lexer import RegexLexer
from pygments.styles import get_style_by_name
from pygments.token import Name, Operator

from addons.ai.src.assistant.utils.abstract_assistant_child import (
    AbstractAssistantChild,
)
from addons.ai.src.assistant.utils.globals import AI_COMMAND_PREFIX
from addons.ai.src.assistant.utils.prompt_pygment_style import PromptPygmentStyle
from src.helper.html import html_remove_tags

if TYPE_CHECKING:
    from addons.ai.src.assistant.assistant import Assistant


class AssistantChatCompleter(Completer):
    def __init__(self, commands: Dict[str, Any]) -> None:
        self.active_commands = commands

    def get_completions(
        self, document: ToolkitDocument, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        word_before_cursor = document.get_word_before_cursor(WORD=True)

        # Previous word was a space
        if word_before_cursor == "":
            return

        parts = word_before_cursor.split(":")
        for command in self.active_commands:
            prefixed_command = f"{AI_COMMAND_PREFIX}{command}"

            if parts[0] == prefixed_command:
                if (isinstance(self.active_commands[command], dict)
                    and "options" in self.active_commands[command]):
                    for option in self.active_commands[command]["options"]:
                        yield Completion(
                            prefixed_command + f":{option} ",
                            start_position=-len(word_before_cursor),
                        )
            elif prefixed_command.startswith(parts[0]):
                if "options" in self.active_commands[command]:
                    pass
                else:
                    prefixed_command += " "

                yield Completion(
                    prefixed_command, start_position=-len(word_before_cursor)
                )


class PromptManager(AbstractAssistantChild):
    """Class to manage a styled command prompt."""

    def __init__(self, assistant: "Assistant") -> None:
        super().__init__(assistant)
        self.prompt = ""
        self.session = PromptSession()
        self.style_name = None
        self.key_bindings = KeyBindings()
        self.setup_key_bindings()

    def contains_any_active_command(self, text: str) -> bool:
        commands = self.assistant.get_active_commands()
        prefix = AI_COMMAND_PREFIX

        # Normalize the text by stripping and adding one space at both ends (simplifies boundary checks)
        normalized_text = f" {text.strip()} "

        for command in commands:
            # Check if the command is at the beginning, in the middle, or at the end of the text
            # We look for the command with a space before and after, or at the text boundaries
            if f" {prefix}{command} " in normalized_text:
                return True

        return False

    def setup_key_bindings(self) -> None:
        """Configure key bindings for handling prompt interactions."""

        @self.key_bindings.add("escape", "enter")
        def _(event: KeyPressEvent) -> None:
            event.current_buffer.insert_text("\n")

        @self.key_bindings.add("enter")
        def _(event: KeyPressEvent) -> None:
            event.current_buffer.validate_and_handle()

    def get_full_text(self) -> str:
        """
        Return the concatenation of text from actual prompt and remaining buffer text.
        :return:
        """
        prompt_chunk = self.session.app.current_buffer.text
        prompt_chunk = html.escape(prompt_chunk)

        for command in self.assistant.get_active_commands():
            prompt_chunk = prompt_chunk.replace(
                f"{AI_COMMAND_PREFIX}{command}",
                f"<command>{AI_COMMAND_PREFIX}{command}</command>",
            )

        return self.prompt + prompt_chunk

    def get_prompt(self):
        """Generate the current styled prompt."""
        return HTML("<prefix>&gt;&gt;&gt; </prefix>" + self.prompt)

    def create_completer(self) -> AssistantChatCompleter:
        return AssistantChatCompleter(self.assistant.get_active_commands())

    def open(self) -> str:
        commands_tokens = {
            "root": [],
            "option": [(r":([a-zA-Z0-9-_]+)", Operator, "#pop")],
        }

        commands = self.assistant.get_active_commands()
        for command, description in commands.items():
            commands_tokens["root"].append(
                (rf"(^|(?<=\s))/\b{command}\b", Name.Builtin, "option")
            )

        class PromptLexer(RegexLexer):
            name = "Prompt Lexer"
            tokens = commands_tokens

        if self.assistant.colors_theme:
            style = get_style_by_name(self.assistant.colors_theme)
        else:
            style = PromptPygmentStyle

        initial_message = ""
        if self.assistant.last_prompt_sections:
            last_section = self.assistant.last_prompt_sections[-1]
            last_command_key = last_section.command

            if last_section.command:
                last_command = commands[last_command_key]
                if isinstance(last_command, dict) and "sticky" in last_command and last_command["sticky"]:
                    initial_message = AI_COMMAND_PREFIX + last_command_key

                    if len(last_section.options):
                        initial_message += ":" + (":".join(last_section.options))

                    initial_message += " "

        """Start the prompt session."""
        self.session.prompt(
            message=self.get_prompt,
            default=initial_message,
            completer=self.create_completer(),
            style=style_from_pygments_cls(style),
            key_bindings=self.key_bindings,
            multiline=True,
            lexer=PygmentsLexer(PromptLexer),
        )

        response = html_remove_tags(self.get_full_text())
        self.prompt = ""

        return response
