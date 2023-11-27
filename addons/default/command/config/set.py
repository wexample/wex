import os
from typing import TYPE_CHECKING

from src.const.globals import CONFIG_SEPARATOR_DEFAULT
from src.decorator.command import command
from src.decorator.option import option

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Set config value to given file")
@option("--file", "-f", type=str, required=True)
@option("--key", "-k", type=str, required=True)
@option("--value", "-v", required=True)
@option("--separator", "-s", required=True, default=CONFIG_SEPARATOR_DEFAULT)
def default__config__set(
    kernel: "Kernel", file, key, value, separator: str = CONFIG_SEPARATOR_DEFAULT
):
    with open(file, "r") as f:
        lines = f.readlines()

    updated_lines = []
    found_key = False

    for line in lines:
        if line.startswith(f"{key}{separator}"):
            updated_lines.append(f"{key}{separator}{value}{os.linesep}")
            found_key = True
        else:
            updated_lines.append(line)

    if not found_key:
        # Add a new line if the file doesn't end with a newline
        if lines and not lines[-1].endswith(os.linesep):
            updated_lines.append(os.linesep)
        # Add a new line if the file doesn't contain any content
        if not lines:
            updated_lines.append(os.linesep)
        updated_lines.append(f"{key}{separator}{value}{os.linesep}")

    with open(file, "w") as f:
        f.writelines(updated_lines)
