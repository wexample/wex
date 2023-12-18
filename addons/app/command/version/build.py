from typing import TYPE_CHECKING, Optional

from git import Repo  # type: ignore

from addons.app.decorator.app_command import app_command
from addons.default.command.version.increment import default__version__increment
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Build a new version of current app")
@option(
    "--version",
    "-v",
    type=str,
    required=False,
    help="New version number, auto generated if missing",
)
@option(
    "--commit",
    "-ok",
    required=False,
    is_flag=True,
    default=False,
    help="New version changes has been validated, ask to commit changes",
)
def app__version__build(
    manager: "AppAddonManager",
    app_dir: str,
    version: Optional[str] = None,
    commit: bool = False,
) -> Optional[str]:
    kernel = manager.kernel

    if not commit:
        if version:
            new_version = version
        else:
            new_version = kernel.run_function(
                default__version__increment,
                {"version": manager.get_config("global.version").get_str()},
            ).print_wrapped_str()

        # Save new version
        kernel.io.log(f"New app version : {new_version}")

        manager.set_config("global.version", new_version)

        kernel.run_command(".version/build", quiet=True)
    else:
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
        latest_tag = tags[-1]

        if str(latest_tag) == new_version:
            kernel.io.error(
                f"The version {new_version} has been already tagged, you should create a new version.",
                trace=False,
            )

        kernel.io.log("Committing new version...")
        try:
            repo.index.add(".wex/config")
            repo.index.commit(f"New version v{new_version}")
            repo.create_tag(f"{new_version}")

            # origin.push()
        except Exception as e:
            kernel.io.error("Git commit : " + str(e), trace=False)

        kernel.io.message(f"New version : {new_version}")

    return new_version
