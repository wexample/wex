from addons.app.command.app.start import app__app__start
from addons.app.command.app.stop import app__app__stop
from src.core.Kernel import Kernel
from addons.app.decorator.app_command import app_command
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse


@app_command(help="Restarts app")
def app__app__restart(kernel: Kernel, app_dir: str):
    def _app__app__restart__stop(previous=None):
        kernel.run_function(
            app__app__stop,
            {
                'app-dir': app_dir
            }
        )

    def _app__app__restart__start(previous=None):
        kernel.run_function(
            app__app__start,
            {
                'app-dir': app_dir
            }
        )

    return QueuedCollectionResponse(kernel, [
        _app__app__restart__stop,
        _app__app__restart__start,
    ])
