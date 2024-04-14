# This is a pure test file in order to quickly test and develop prompt styling
# python3 addons/as/tests/prompt.py

from prompt_toolkit.shortcuts import PromptSession

session = PromptSession()

from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.styles import Style
from prompt_toolkit import HTML
import datetime


def talk():
    kb = KeyBindings()
    prompt = ""

    @kb.add("<any>")
    def _(event: KeyPressEvent) -> None:
        nonlocal prompt

        if event.data in ["d"]:
            prompt += event.current_buffer.text + "d"
            event.current_buffer.text = ""

            prompt = prompt.replace(" world", " <world>world</world>")
        else:
            event.app.current_buffer.insert_text(event.data)

        session.app.invalidate()

    style = Style.from_dict({
        'world': 'fg:green'
    })

    def get_prompt():
        nonlocal prompt
        now = datetime.datetime.now()
        return HTML("<prefix>&gt;&gt;&gt; </prefix>"
                    + prompt)

    session.prompt(
        get_prompt,
        style=style,
        key_bindings=kb)


talk()
