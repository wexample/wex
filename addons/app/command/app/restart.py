from typing import TYPE_CHECKING

from addons.app.command.app.start import app__app__start
from addons.app.command.app.stop import app__app__stop
from addons.app.decorator.app_command import app_command
from src.core.response.AbstractResponse import AbstractResponse
from src.decorator.option import option
from src.helper.prompt import prompt_progress_steps

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Restarts app")
@option("--fast", "-f", is_flag=True, required=False, help="Do not rewrite config")
def app__app__restart(
    manager: "AppAddonManager",
    app_dir: str,
    fast: bool = False,
) -> None:
    kernel = manager.kernel
    options = {"app-dir": app_dir, "fast": fast}

    def _app__app__restart__stop() -> AbstractResponse:
        return kernel.run_function(app__app__stop, options)

    def _app__app__restart__start() -> AbstractResponse:
        return kernel.run_function(app__app__start, options)

    prompt_progress_steps(
        kernel,
        [
            _app__app__restart__stop,
            _app__app__restart__start,
        ],
    )
