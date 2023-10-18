from addons.app.command.app.start import app__app__start
from addons.app.command.app.stop import app__app__stop
from src.decorator.alias_without_addon import alias_without_addon
from src.core.Kernel import Kernel
from addons.app.decorator.app_command import app_command


@app_command(help="Restarts app")
@alias_without_addon()
def app__app__restart(kernel: Kernel, app_dir: str):
    kernel.run_function(
        app__app__stop,
        {
            'app-dir': app_dir
        }
    )

    kernel.run_function(
        app__app__start,
        {
            'app-dir': app_dir
        }
    )
