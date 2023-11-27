from typing import TYPE_CHECKING

from addons.app.command.app.start import app__app__start
from addons.app.command.app.stop import app__app__stop
from addons.app.decorator.app_command import app_command
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Restarts app")
def app__app__restart(manager: "AppAddonManager", app_dir: str):
    kernel = manager.kernel

    def _app__app__restart__stop(previous=None):
        return kernel.run_function(app__app__stop, {"app-dir": app_dir})

    def _app__app__restart__start(previous=None):
        return kernel.run_function(app__app__start, {"app-dir": app_dir})

    return QueuedCollectionResponse(
        kernel,
        [
            _app__app__restart__stop,
            _app__app__restart__start,
        ],
    )
