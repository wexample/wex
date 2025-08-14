from typing import TYPE_CHECKING

from git import Repo

from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_ADDON

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Description", command_type=COMMAND_TYPE_ADDON)
def app__version__new_commit(manager: "AppAddonManager", app_dir: str) -> None:
    kernel = manager.kernel
    repo = Repo(app_dir)
    new_version = manager.get_config("global.version").get_str()

    if not repo.is_dirty(untracked_files=True):
        kernel.io.log("No changes to commit")
        return None

    # Commit directly on the current branch without switching branches
    kernel.io.log("Committing new version...")
    try:
        repo.git.add(A=True)
        repo.index.commit(f"New version v{new_version}")
    except Exception as e:
        kernel.io.error("Git commit : " + str(e), trace=False)

    kernel.io.message(f"New version : {new_version}")
