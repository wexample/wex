import os
from typing import TYPE_CHECKING

import git

from addons.app.command.config.set import app__config__set
from addons.app.command.version.build import app__version__build
from addons.app.const.app import APP_FILEPATH_REL_CONFIG
from addons.default.command.version.increment import default__version__increment
from addons.default.const.default import UPGRADE_TYPE_MINOR
from src.const.globals import CORE_COMMAND_NAME, FILE_README, FILE_VERSION
from src.decorator.command import command
from src.decorator.option import option
from src.helper.core import core_kernel_get_version

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Build a new version of current core, or commit new version changes")
@option(
    "--commit",
    "-ok",
    required=False,
    is_flag=True,
    default=False,
    help="New version changes has been validated, ask to commit changes",
)
@option("--type", "-t", type=str, required=False, help="Type of update")
def core__version__build(
    kernel: "Kernel", commit: bool = False, type: str = UPGRADE_TYPE_MINOR
) -> None:
    version = core_kernel_get_version(kernel)
    root_dir = kernel.get_path("root")
    repo = git.Repo(root_dir)

    if not commit:
        current_version = core_kernel_get_version(kernel)

        kernel.io.log(f"Executing auto formatting scripts...")
        kernel.run_command(
            '.code/format',
            {
                'app_dir': root_dir
            }
        )

        kernel.io.log(f"Building new version from {current_version}...")

        # There is no uncommitted change
        if repo.is_dirty(untracked_files=True):
            kernel.io.error(
                "{diff}"
                + os.linesep
                + "There is uncommitted changes in the repository",
                {"diff": repo.git.diff()},
                trace=False,
            )

        kernel.io.log(f"Executing code quality checkup...")
        kernel.run_command(
            '.code/check',
            {
                'app_dir': root_dir
            }
        )

        new_version = kernel.run_function(
            default__version__increment,
            {
                "version": version,
                "build": True,
                "type": type,
            },
        ).first()

        # Write new_version to file
        with open(f"{root_dir}{FILE_VERSION}", "w") as version_file:
            version_file.write(str(new_version))

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
            app__version__build, {"version": new_version, "app-dir": root_dir}
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

        kernel.io.message_next_command(core__version__build, {"commit": True})

    else:
        if not repo.is_dirty(untracked_files=True):
            kernel.io.log("No changes to commit")
            return

        repo.index.add(root_dir + FILE_VERSION)
        repo.index.add(root_dir + FILE_README)
        repo.index.add(root_dir + APP_FILEPATH_REL_CONFIG)

        kernel.run_function(
            app__version__build, {"commit": commit, "app-dir": root_dir}
        )
