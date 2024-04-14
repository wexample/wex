# This is a pure test file in order to quickly test and develop prompt styling
# python3 addons/as/tests/prompt.py
import html
import re

from prompt_toolkit import HTML
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.styles import Style


def talk():
    kb = KeyBindings()
    prompt = ""

    def remove_tags(text):
        # Use a regular expression to find and remove tags
        # This regex matches anything that looks like HTML/XML tag and replaces it with an empty string
        return re.sub(r'<[^>]*>', '', text)

    def split_prompt_parts(prompt_body: str) -> list[str]:
        parts = re.split(r'(<[^>]*>[^<]*<\/[^>]*>)', prompt_body)
        parts = [part for part in parts if part.strip()]
        result = []

        if not len(parts):
            return []

        temp = parts[0]
        for part in parts[1:]:
            if '<' in part and '>' in part:
                temp += part
            else:
                result.append(temp)
                temp = part
        result.append(temp)
        return result

    @kb.add("backspace")
    def handle_key(event: KeyPressEvent) -> None:
        nonlocal prompt

        if event.current_buffer.text == "":
            chunks = split_prompt_parts(prompt)

            if len(chunks):
                prompt = ''.join(chunks[:-1])

                event.current_buffer.insert_text(
                    html.unescape(remove_tags(chunks[-1])),
                    overwrite=True
                )

        event.app.current_buffer.delete_before_cursor()

        session.app.invalidate()

    @kb.add("<any>")
    def handle_key(event: KeyPressEvent) -> None:
        nonlocal prompt

        if event.data in ["d"]:
            prompt_chunk = event.current_buffer.text + event.data
            prompt_chunk = html.escape(prompt_chunk)
            prompt_chunk = prompt_chunk.replace(" world", " <world>world</world>")
            event.current_buffer.text = ""

            prompt += prompt_chunk
        else:
            event.app.current_buffer.insert_text(event.data)

        session.app.invalidate()

    style = Style.from_dict({
        'world': 'fg:green'
    })

    def get_prompt():
        nonlocal prompt

        return HTML("<prefix>&gt;&gt;&gt; </prefix>"
                    + prompt)

    # Create a session with the prompt function, styling, and key bindings
    session = PromptSession()
    session.prompt(
        get_prompt,
        style=style,
        key_bindings=kb)


talk()
