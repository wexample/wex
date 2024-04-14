import html
from typing import TYPE_CHECKING, Iterable

from prompt_toolkit import HTML
from prompt_toolkit.completion import CompleteEvent, Completer, Completion
from prompt_toolkit.document import Document as ToolkitDocument
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
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
        for command in self.assistant.get_active_commands():
            if f"{AI_COMMAND_PREFIX}{command}" in text:
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

        @self.key_bindings.add("backspace")
        def handle_backspace(event: KeyPressEvent) -> None:
            """Handle backspace key to manage prompt text."""
            if event.current_buffer.text == "":
                parts = html_split_prompt_parts(self.prompt)
                if parts:
                    self.prompt = ''.join(parts[:-1])
                    event.current_buffer.insert_text(
                        html.unescape(html_remove_tags(parts[-1])),
                        overwrite=True
                    )
                return
            event.app.current_buffer.delete_before_cursor()
            self.session.app.invalidate()

        @self.key_bindings.add("<any>")
        def handle_any(event: KeyPressEvent) -> None:
            if self.contains_any_active_command(event.current_buffer.text):
                self.session.app.current_buffer.text += event.data
                self.prompt = self.get_full_text()
                self.session.app.current_buffer.text = ""
            else:
                event.app.current_buffer.insert_text(event.data)
            self.session.app.invalidate()

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
        """Start the prompt session."""
        self.session.prompt(
            self.get_prompt,
            completer=self.create_completer(),
            style=self.style,
            key_bindings=self.key_bindings,
            multiline=True,
        )

        return html_remove_tags(self.get_full_text())
