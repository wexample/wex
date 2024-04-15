import html
from typing import TYPE_CHECKING, Iterable

from prompt_toolkit import HTML
from prompt_toolkit.completion import CompleteEvent, Completer, Completion
from prompt_toolkit.document import Document as ToolkitDocument
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.styles import Style

from addons.ai.src.assistant.utils.abstract_assistant_child import AbstractAssistantChild
from addons.ai.src.assistant.utils.globals import AI_COMMAND_PREFIX
from src.const.types import StringsList
from src.helper.html import html_remove_tags, html_split_prompt_parts

if TYPE_CHECKING:
    from addons.ai.src.assistant.assistant import Assistant


class AssistantChatCompleter(Completer):
    def __init__(self, commands: StringsList) -> None:
        self.active_commands = commands

    def get_completions(
        self, document: ToolkitDocument, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        word_before_cursor = document.get_word_before_cursor(WORD=True)

        # Previous word was a space
        if word_before_cursor == "":
            return

        for command in self.active_commands:
            if command.startswith(word_before_cursor):
                yield Completion(command + " ", start_position=-len(word_before_cursor))


class PromptManager(AbstractAssistantChild):
    """Class to manage a styled command prompt."""

    def __init__(self, assistant: "Assistant"):
        super().__init__(assistant)
        self.prompt = ""
        self.session = PromptSession()
        self.style = Style.from_dict({
            'prefix': '#666 bold',
            'command': 'fg:#60A9F7'
        })
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

    def setup_key_bindings(self):
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
                f"<command>{AI_COMMAND_PREFIX}{command}</command>")

        return self.prompt + prompt_chunk

    def get_prompt(self):
        """Generate the current styled prompt."""
        return HTML("<prefix>&gt;&gt;&gt; </prefix>" + self.prompt)

    def create_completer(self) -> AssistantChatCompleter:
        return AssistantChatCompleter(
            [f"{AI_COMMAND_PREFIX}{command}" for command in self.assistant.get_active_commands()]
        )

    def open(self) -> str:
        from pygments.lexer import RegexLexer
        from pygments.token import Generic

        commands_tokens = {'root': []}
        commands = self.assistant.get_active_commands()
        for command, description in commands.items():
            pattern = rf'(^|(?<=\s))/\b{command}\b'
            style = Generic.Inserted
            token_tuple = (pattern, style)
            commands_tokens['root'].append(token_tuple)

        class PromptLexer(RegexLexer):
            name = 'Prompt Lexer'
            tokens = commands_tokens

        """Start the prompt session."""
        self.session.prompt(
            self.get_prompt,
            completer=self.create_completer(),
            style=self.style,
            key_bindings=self.key_bindings,
            multiline=True,
            lexer=PygmentsLexer(PromptLexer)
        )

        response = html_remove_tags(self.get_full_text())
        self.prompt = ""

        return response
