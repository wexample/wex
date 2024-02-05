from typing import TYPE_CHECKING

from addons.app.command.app.start import app__app__start
from addons.app.command.app.stop import app__app__stop
from addons.app.decorator.app_command import app_command
from src.core.response.AbstractResponse import AbstractResponse
from src.core.response.queue_collection.AbstractQueuedCollectionResponseQueueManager import (
    AbstractQueuedCollectionResponseQueueManager,
)
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Restarts app")
@option("--fast", "-f", is_flag=True, required=False, help="Do not rewrite config")
def app__app__restart(
    manager: "AppAddonManager",
    app_dir: str,
    fast: bool = False,
) -> QueuedCollectionResponse:
    kernel = manager.kernel
    options = {
        "app-dir": app_dir,
        "fast": fast
    }

    def _app__app__restart__stop(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> AbstractResponse:
        return kernel.run_function(app__app__stop, options)

    def _app__app__restart__start(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> AbstractResponse:
        return kernel.run_function(app__app__start, options)

    return QueuedCollectionResponse(
        kernel,
        [
            _app__app__restart__stop,
            _app__app__restart__start,
        ],
    )
