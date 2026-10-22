from __future__ import annotations

import os
import shutil
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_wex_core.common.kernel import Kernel

_ART_LINES = [
    ".o%%%o.",
    ".%%%%%%%%%%%%%%.",
    ".&&&%%%%%%%%%%%%%%%%%%%%%.",
    "&&&&&&&%%%%%%%%%%%%%%%%%%%%%%%%%",
    "&&&&&&/    %%%%%%%%%%%%   \\%%%%%%%",
    "&&&&&&     %%%%%%%%%%%%     %%%%%%",
    "&&&&&&     &&&&&%%%%%%%     %%%%%%",
    "&&&&&&     &&&`    `&&&     %%&&&&",
    "&&&&&&./&                &\\.&&&&&&",
    "&&&&&&&&@      .&&.      &&&&&&&&&",
    " &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",
    "`&&&&&&&&&&&&&&&&&&&&&&&&`",
    "`&&&&&&&&&&&&&&`",
    "`°&&&&°`",
]

_WORDMARK_LINES = [
    ".-..-..--. .--. .-.,-.  ",
    ": `; `;  :' '_.'`.  .'  ",
    "`.__.__._'`.__.':_,._;  ",
]


def _center(line: str, width: int) -> str:
    pad = max(0, (width - len(line)) // 2)
    return " " * pad + line


def get_logo(kernel: "Kernel") -> str:
    from wexample_prompt.enums.terminal_color import TerminalColor

    R = str(TerminalColor.RED)
    GRAY = str(TerminalColor.LIGHT_BLACK)
    RESET = str(TerminalColor.RESET)

    width = shutil.get_terminal_size((80, 24)).columns
    sep = os.linesep

    version = ""
    if hasattr(kernel, "get_version"):
        try:
            version = f"v{kernel.get_version()}"
        except Exception:
            pass

    lines = [sep]

    for line in _ART_LINES:
        lines.append(R + _center(line, width) + RESET)

    lines.append("")

    for line in _WORDMARK_LINES:
        lines.append(R + _center(line.rstrip(), width) + RESET)

    lines.append("")

    tagline = "★  www.wexample.com  ★"
    if version:
        tagline += f"   {version}"
    lines.append(GRAY + _center(tagline, width) + RESET)
    lines.append(sep)

    return sep.join(lines)
