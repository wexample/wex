import shutil
import os

from src.helper.prompt import prompt_choice

TEXT_ALIGN_LEFT = "left"
TEXT_ALIGN_RIGHT = "right"
MAX_WIDTH = 250


def chat_format_message(
    text: str,
    align: str = TEXT_ALIGN_LEFT,
    padding: int = 1,
    max_width: int = MAX_WIDTH,
) -> str:
    padding_horizontal_char = "    "
    terminal_width = shutil.get_terminal_size().columns
    max_text_width = min(
        max_width, terminal_width - len(padding_horizontal_char) * 2 * padding - 2
    )

    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 > max_text_width:
            lines.append(current_line)
            current_line = word
        else:
            if current_line:
                current_line += " "
            current_line += word
    if current_line:
        lines.append(current_line)

    frame_width = (
        max(len(line) for line in lines)
        + len(padding_horizontal_char) * 2 * padding
        + 2
    )
    frame_width = min(frame_width, terminal_width)

    top_bottom_frame = "+" + "-" * (frame_width - 2) + "+"
    horizontal_padding = "|" + " " * (frame_width - 2) + "|"
    formatted_lines = [
        "|"
        + padding_horizontal_char * padding
        + line.ljust(frame_width - len(padding_horizontal_char) * 2 * padding - 2)
        + padding_horizontal_char * padding
        + "|"
        for line in lines
    ]

    frame = (
        [top_bottom_frame]
        + [horizontal_padding] * padding
        + formatted_lines
        + [horizontal_padding] * padding
        + [top_bottom_frame]
    )

    if align == TEXT_ALIGN_RIGHT:
        frame = [line.rjust(terminal_width) for line in frame]

    return "\n".join(frame)


def chat_help(kernel: "Kernel") -> None:
    kernel.io.message("Welcome to chat mode")
    kernel.io.log("  Type '/action' to pick an action.")
    kernel.io.log("  Type '/model' change used model.")
    kernel.io.log("  Type '/?' or '/help' to display this message again.")
    kernel.io.log("  Type '/exit' to quit.")


def chat_quit(kernel: "Kernel") -> None:
    kernel.io.log(f"{os.linesep}Ciao")


CHAT_ACTION_FREE_TALK = "FREE_TALK"
CHAT_ACTION_FREE_TALK_FILE = "TALK_FILE"
CHAT_ACTION_LAST = "ACTION_LAST"

CHAT_ACTIONS_TRANSLATIONS = {
    CHAT_ACTION_FREE_TALK: "> Free Talk",
    CHAT_ACTION_FREE_TALK_FILE: "> Talk about a file",
    CHAT_ACTION_LAST: "> Last action"
}


def chat_choose_action() -> str:
    choice = prompt_choice(
        "Choose an action to do with ai assistant :",
        [
            CHAT_ACTIONS_TRANSLATIONS[CHAT_ACTION_FREE_TALK],
            CHAT_ACTIONS_TRANSLATIONS[CHAT_ACTION_FREE_TALK_FILE],
            CHAT_ACTIONS_TRANSLATIONS[CHAT_ACTION_LAST],
        ],
    )

    # TODO Now returned choice is the translation like "> Talk about a file", I would like to get the key TALK_FILE

    return choice
