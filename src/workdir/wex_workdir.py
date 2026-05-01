from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class
from wexample_wex_addon_app.workdir.code_base_workdir import CodeBaseWorkdir
from wexample_wex_core.workdir.kernel_workdir import KernelWorkdir


@base_class
class WexWorkdir(
    CodeBaseWorkdir,
    KernelWorkdir
):
    """
    The main wex core kernel is also an app kernel (with .wex config, etc.)
    """

    def apply(self, **kwargs):
        # CodeBaseWorkdir.apply() delegates to manager_run_command (app-manager subprocess).
        # WexWorkdir is the kernel itself — skip to the filestate apply directly.
        from wexample_wex_addon_app.workdir.managed_workdir import ManagedWorkdir

        return super(ManagedWorkdir, self).apply(**kwargs)

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

        super().publish(force=force)
