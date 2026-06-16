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

    def get_src_import_name(self) -> str | None:
        # wex is a CLI app, not a distributable package — `src/` contains
        # `common/`, `workdir/`, etc. directly, no single `src/wex/` module.
        # Returning None tells PythonPyprojectTomlFile to skip the
        # packaging/coverage enforces that would otherwise write
        # `packages=[{include: 'wex', from: 'src'}]` and
        # `coverage.source = ['wex']` — both nonsensical here.
        return None

    def bump(self, interactive: bool = False, force: bool = False, **kwargs) -> bool:
        # wex changes are driven by its packages (separate repos), so git change
        # detection on the wex directory alone would miss them — always force bump.
        return super().bump(interactive=interactive, force=True, **kwargs)

    def release(
        self,
        force: bool = False,
        interactive: bool = True,
        has_changes=None,
        skip_test: bool = False,
    ) -> None:
        from wexample_wex_addon_app.commands.library.sync import app__library__sync
        from wexample_wex_addon_package.commands.suite.publish import (
            package__suite__publish,
        )

        library_path = self.get_env_parameter("PROGRAM_PUBLICATION_SOURCE_LIBRARY_PATH")

        if library_path:
            arguments = ["--yes"]
            if skip_test:
                arguments.append("--skip-test")
            self.manager_run_command_from_path(
                command=package__suite__publish,
                path=library_path,
                arguments=arguments,
            )
            self.manager_run_command(command=app__library__sync)

        super().release(
            force=force,
            interactive=interactive,
            has_changes=has_changes,
            skip_test=skip_test,
        )
