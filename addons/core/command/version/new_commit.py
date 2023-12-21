from typing import TYPE_CHECKING

from git import Repo  # type: ignore

from addons.app.command.version.new_commit import app__version__new_commit
from addons.app.const.app import APP_FILEPATH_REL_CONFIG
from src.const.globals import FILE_README, FILE_VERSION
from src.decorator.command import command
from src.decorator.option import option

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Build a new version of current core, or commit new version changes")
@option("--type", "-t", type=str, required=False, help="Type of update")
def core__version__new_commit(
    kernel: "Kernel", commit: bool = False
) -> None:
    root_dir = kernel.directory.path
    repo = Repo(root_dir)

    if not repo.is_dirty(untracked_files=True):
        kernel.io.log("No changes to commit")
        return None

    repo.index.add(root_dir + FILE_VERSION)
    repo.index.add(root_dir + FILE_README)
    repo.index.add(root_dir + APP_FILEPATH_REL_CONFIG)

    kernel.run_function(
        app__version__new_commit,
        {"commit": commit, "app-dir": root_dir}
    )
