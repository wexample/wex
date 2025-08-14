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
    main_branch = manager.get_config("git.main_branch", "main").get_str()

    if not repo.is_dirty(untracked_files=True):
        kernel.io.log("No changes to commit")
        return None

    kernel.io.log("Updating repo...")
    try:
        origin = repo.remote(name="origin")
        # Always fetch latest refs and tags first
        origin.fetch(tags=True)

        # Ensure local main branch is safely aligned with origin without implicit merges
        current_branch = repo.active_branch.name
        # Checkout main (create tracking branch if missing)
        if main_branch in [h.name for h in repo.heads]:
            repo.git.checkout(main_branch)
        else:
            # Create local main tracking origin/main
            repo.git.checkout("-b", main_branch, f"origin/{main_branch}")

        # Fast-forward only to origin/main to avoid accidental merges
        try:
            repo.git.merge("--ff-only", f"origin/{main_branch}")
        except Exception as ff_err:
            kernel.io.warn(
                f"Cannot fast-forward {main_branch} to origin/{main_branch}: {ff_err}. Leaving branch unchanged.")

        # Go back to the original branch to continue the version commit
        if current_branch != main_branch:
            repo.git.checkout(current_branch)
    except Exception as e:
        kernel.io.error("Git pull : " + str(e), trace=False)

    kernel.io.log("Committing new version...")
    try:
        repo.git.add(A=True)
        repo.index.commit(f"New version v{new_version}")
    except Exception as e:
        kernel.io.error("Git commit : " + str(e), trace=False)

    kernel.io.message(f"New version : {new_version}")
