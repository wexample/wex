import platform
from typing import TYPE_CHECKING

from src.decorator.command import command

if TYPE_CHECKING:
    from src.core.Kernel import Kernel

OS_NAME_LINUX: str = "linux"
OS_NAME_MAC: str = "mac"
OS_NAME_UNDEFINED: str = "undefined"
OS_NAME_WINDOWS: str = "windows"


@command(help="Return the local OS name.")
def system__os__name(kernel: "Kernel") -> str:
    os_name = platform.system()

    if os_name == "Darwin":
        return OS_NAME_MAC
    elif os_name == "Linux":
        return OS_NAME_LINUX
    elif os_name in ["CYGWIN", "MINGW32", "MINGW64", "MSYS"]:
        return OS_NAME_WINDOWS
    else:
        return OS_NAME_UNDEFINED
