from typing import TYPE_CHECKING, cast

from addons.app.command.db.restore import app__db__restore
from addons.app.command.remote.push_receive import (
    _app__remote__push_receive_find_app_dir,
    app__remote__push_receive,
)
from src.const.globals import COMMAND_TYPE_ADDON
from src.core.command.ScriptCommand import ScriptCommand
from src.decorator.attach import attach
from src.decorator.command import command
from src.decorator.option import option

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


@attach(
    position="after",
    command=cast(ScriptCommand, app__remote__push_receive),
    pass_args=["app", "env"],
)
@command(
    help="This command is a bridge between remote/push-receive "
    "and db services for mounting latest updated database dump",
    command_type=COMMAND_TYPE_ADDON,
)
@option(
    "--app", "-a", type=str, required=True, help="Application name, used to find path"
)
@option(
    "--env",
    "-e",
    type=str,
    required=True,
    help="App environment, a same application may exists in various environment",
)
def db__remote__push_restore(
    kernel: "Kernel",
    app: str,
    env: str,
) -> None:
    app_dir = _app__remote__push_receive_find_app_dir(kernel, app, env)

    if not app_dir:
        return

    kernel.run_function(
        app__db__restore, {"app_dir": app_dir, "file-path": "db.latest.zip"}
    )
