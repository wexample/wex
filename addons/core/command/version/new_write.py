import os
from typing import TYPE_CHECKING, Optional

from git import Repo

from addons.app.command.code.format import app__code__format
from addons.app.command.config.set import app__config__set
from addons.app.command.version.new_write import app__version__new_write
from addons.core.command.version.new_commit import core__version__new_commit
from addons.default.command.version.increment import default__version__increment
from addons.default.const.default import UPGRADE_TYPE_MINOR
from src.const.globals import CORE_COMMAND_NAME, FILE_README
from src.core.response.AbstractResponse import AbstractResponse
from src.core.response.queue_collection.AbstractQueuedCollectionResponseQueueManager import (
    AbstractQueuedCollectionResponseQueueManager,
)
from src.core.response.queue_collection.QueuedCollectionStopResponse import (
    QueuedCollectionStopResponse,
)
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
from src.decorator.command import command
from src.decorator.option import option
from src.helper.core import core_kernel_get_version

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Build a new version of current core, or commit new version changes")
@option("--type", "-t", type=str, required=False, help="Type of update")
def core__version__new_write(
    kernel: "Kernel", type: str = UPGRADE_TYPE_MINOR
) -> Optional[QueuedCollectionResponse]:
    version = core_kernel_get_version(kernel)
    root_dir = kernel.directory.path
    repo = Repo(root_dir)

    current_version = core_kernel_get_version(kernel)

    def _core__version__build__format(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> AbstractResponse:
        kernel.io.log(f"Executing auto formatting scripts...")

        return kernel.run_function(app__code__format, {"app-dir": root_dir})

    def _core__version__build__check_uncommitted(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> Optional[QueuedCollectionStopResponse]:
        # There is no uncommitted change
        if repo.is_dirty(untracked_files=True):
            kernel.io.error(
                "{diff}"
                + os.linesep
                + "There is uncommitted changes in the repository",
                {"diff": repo.git.diff()},
                trace=False,
            )

            return QueuedCollectionStopResponse(kernel, "Dirty repository")

        return None

    def _core__version__build__increment_version(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> None:
        kernel.io.log(f"Building new version from {current_version}...")

        new_version = kernel.run_function(
            default__version__increment,
            {
                "version": version,
                "build": True,
                "type": type,
                # Just regenerate a build number
                "increment": 0,
            },
        ).first()

        # Set wex version for itself.
        kernel.run_function(
            app__config__set,
            {
                "app-dir": root_dir,
                "key": f"{CORE_COMMAND_NAME}.version",
                "value": new_version,
            },
        )

        # Enforce new version for wex app.
        kernel.run_function(
            app__version__new_write, {"version": new_version, "app-dir": root_dir}
        )

        # Update README.md
        readme_path = os.path.join(root_dir, FILE_README)

        with open(readme_path, "r") as file:
            readme_content = file.read()

        # Replace old version with new version
        updated_content = readme_content.replace(
            "wex v" + version, "wex v" + new_version
        )

        with open(readme_path, "w") as file:
            file.write(updated_content)

        kernel.io.message_next_command(core__version__new_commit)

    return QueuedCollectionResponse(
        kernel,
        [
            _core__version__build__format,
            _core__version__build__check_uncommitted,
            _core__version__build__increment_version,
        ],
    )
