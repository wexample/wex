from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.command import command
from src.decorator.option import option
from typing import TYPE_CHECKING
from addons.app.decorator.app_command import app_command

from git import Repo  # type: ignore

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Description", command_type=COMMAND_TYPE_ADDON)
def app__version__new_commit(
    manager: "AppAddonManager",
    app_dir: str) -> None:
    kernel = manager.kernel
    repo = Repo(app_dir)
    new_version = manager.get_config("global.version").get_str()

    if not repo.is_dirty(untracked_files=True):
        kernel.io.log("No changes to commit")
        return None

    kernel.io.log("Updating repo...")
    try:
        origin = repo.remote(name="origin")
        origin.fetch(tags=True)
        origin.pull()
    except Exception as e:
        kernel.io.error("Git pull : " + str(e), trace=False)

    # Get the last tag.
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
    if len(tags):
        latest_tag = tags[-1]

        if str(latest_tag) == new_version:
            kernel.io.error(
                f"The version {new_version} has been already tagged, you should create a new version.",
                trace=False,
            )

    kernel.io.log("Committing new version...")
    try:
        repo.git.add(A=True)
        repo.index.commit(f"New version v{new_version}")
        repo.create_tag(f"{new_version}")
    except Exception as e:
        kernel.io.error("Git commit : " + str(e), trace=False)

    kernel.io.message(f"New version : {new_version}")
