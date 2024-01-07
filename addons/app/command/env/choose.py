from InquirerPy.base.control import Choice
from typing import List, cast, Optional, TYPE_CHECKING
from src.helper.prompt import prompt_choice
from src.decorator.option import option
from addons.app.const.app import (
    APP_ENV_LOCAL,
    APP_ENVS
)
from addons.app.decorator.app_command import app_command
from src.core.response.queue_collection.QueuedCollectionStopResponse import (
    AbortResponse,
)
from addons.app.command.env.set import app__env__set

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Ask user about which environment to use")
@option('--question', '-q', type=str, required=True, help="Question to ask to user")
def app__env__choose(manager: "AppAddonManager", app_dir: str, question: str = "Choose app environment") -> Optional[
    AbortResponse]:
    env = prompt_choice(
        question,
        cast(List[str | Choice], APP_ENVS),
        APP_ENV_LOCAL,
    )

    # User said "no" or chose "abort"
    if not env:
        manager.log("Abort")
        return AbortResponse(manager.kernel, "USER_ABORT_CONFIGURATION")

    manager.kernel.run_function(
        app__env__set, {
            'app_dir': manager.get_app_dir(),
            "environment": env
        })
