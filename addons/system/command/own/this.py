import os
from typing import TYPE_CHECKING, Optional

from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from src.decorator.option import option
from src.helper.user import get_user_or_sudo_user, set_owner_recursively

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


@as_sudo()
@command(
    help="Make current user owner of this directory and every files or subdirectories"
)
@option("--path", "-p", type=str, required=False, default=None, help="Argument")
def system__own__this(kernel: "Kernel", path: Optional[str] = None) -> None:
    if path is None:
        path = os.getcwd()

    kernel.io.log(
        f'Setting recursively ownership to "{get_user_or_sudo_user()}" on : {path}'
    )
    set_owner_recursively(path)
