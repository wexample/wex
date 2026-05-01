from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_wex_addon_dev_python.workdir.python_workdir import PythonWorkdir

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


class AppWorkdir(PythonWorkdir):
    """
    App-level workdir for the wex project, loaded by the app-manager subprocess.

    IMPORTANT: this is the class that addon commands receive as `app_workdir`
    when run from the wex project directory (via AppMiddleware). It is NOT
    the same as WexWorkdir (src/workdir/wex_workdir.py), which is the kernel-level
    workdir and is never seen by addon commands.

    All project-specific overrides (publish, bump, etc.) belong here.
    """
    def prepare_value(self, raw_value: DictConfig | None = None) -> DictConfig:
        raw_value = super().prepare_value(raw_value=raw_value)

        # wex is a CLI app, not a standard Python package — it does not follow
        # the src/{vendor}_{name}/ layout enforced by PythonWorkdir.
        raw_value["children"] = [
            child
            for child in raw_value["children"]
            if not (isinstance(child, dict) and child.get("name") == "src")
        ]

        return raw_value

    def get_package_import_name(self) -> str:
        return "wex"

    def get_package_name(self) -> str:
        return "wex"

    def bump(self, interactive: bool = False, force: bool = False, **kwargs) -> bool:
        # wex changes are driven by its packages (separate repos), so git change
        # detection on the wex directory alone would miss them — always force bump.
        return super().bump(interactive=interactive, force=True, **kwargs)

    def publish(self, force: bool = False) -> None:
        import os

        from wexample_wex_addon_app.commands.library.sync import app__library__sync
        from wexample_wex_addon_app.commands.state.rectify import app__state__rectify
        from wexample_wex_addon_package.commands.suite.publish import (
            package__suite__publish,
        )

        library_path = os.environ.get("PROGRAM_PUBLICATION_SOURCE_LIBRARY_PATH")

        if library_path:
            self.manager_run_command_from_path(
                command=package__suite__publish,
                path=library_path,
                arguments=["--yes"],
            )
            self.manager_run_command(command=app__library__sync)

        bumped = self.bump(interactive=False, force=force)
        if not bumped:
            return

        self.manager_run_command(command=app__state__rectify, arguments=["--loop", "--yes"])
        self.commit_changes()
        self.push_to_deployment_remote()

        # bump() already gated publication — skip the redundant should_be_published() check
        super().publish(force=True)
