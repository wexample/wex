import os
import re
from typing import TYPE_CHECKING

from src.const.globals import CONFIG_SEPARATOR_DEFAULT
from src.decorator.command import command
from src.decorator.option import option

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Get config value to given file")
@option("--file", "-f", type=str, required=True)
@option("--key", "-k", type=str, required=True)
@option("--separator", "-s", required=True, default=CONFIG_SEPARATOR_DEFAULT)
@option("--default", "-d", default="")
def default__config__get(
    kernel: "Kernel",
    file: str,
    key: str,
    separator: str = CONFIG_SEPARATOR_DEFAULT,
    default: str = "",
) -> str:
    if not file or not os.path.isfile(file):
        return ""

    with open(file, "r") as f:
        lines = f.readlines()

    for line in lines:
        if re.search(r"^\s*" + re.escape(key) + r"\s*" + re.escape(separator), line):
            return re.split(separator, line)[-1].strip()

    return default
