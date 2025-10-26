from __future__ import annotations

from typing import TYPE_CHECKING

from src.decorator.alias import alias
from src.decorator.command import command

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


@alias("-v")
@alias("-version")
@alias("--v")
@alias("--version")
@alias("version")
@command(help="Returns core version")
def core__version__get(kernel: Kernel) -> str:
    from src.helper.core import core_kernel_get_version

    return core_kernel_get_version(kernel)
