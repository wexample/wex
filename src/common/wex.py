from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class
from wexample_wex_core.common.kernel import Kernel

if TYPE_CHECKING:
    from src.workdir.wex_workdir import WexWorkdir

_ASSETS_DIR = Path(__file__).parent.parent.parent / "assets"


@base_class
class Wex(Kernel):
    def get_logo(self) -> str | None:
        import importlib.util

        logo_py = _ASSETS_DIR / "logo.py"
        if not logo_py.exists():
            return None

        spec = importlib.util.spec_from_file_location("wex_logo", logo_py)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
        return mod.get_logo(self)

    def _get_workdir_state_manager_class(self) -> type[WexWorkdir]:
        from src.workdir.wex_workdir import WexWorkdir
        return WexWorkdir

    def exec(self):
        try:
            self.setup(addons=self._discover_addons()).exec_argv()
        except Exception as e:
            from wexample_app.helper.debug import debug_handle_app_error

            debug_handle_app_error(e)

    @classmethod
    def _discover_addons(cls) -> list[type]:
        """The addon managers of every package installed beside wex that declares one.

        Read off the `wex.addons` entry points, which pip writes into a package's
        metadata when it installs it: what wex is made of is decided by what is
        installed in the environment it runs in, and written nowhere here. A bundle
        mounted in a container and installed at its start is an addon like the
        others, and a host and a container that install differently boot
        differently — which is what is wanted of them.

        Sorted by name, so that two environments holding the same packages boot the
        same. A package whose manager does not import is left out and named on
        stderr, not fatal: the others still have to answer, and a worker that dies
        on one bundle at fault serves none of the rest.
        """
        import sys
        from importlib.metadata import entry_points

        classes: list[type] = []

        for entry_point in sorted(entry_points(group="wex.addons"), key=lambda ep: ep.name):
            try:
                classes.append(entry_point.load())
            except Exception as error:
                print(f"Leaving out addon « {entry_point.name} »: {error}", file=sys.stderr)

        return classes or cls._addons_before_entry_points()

    @staticmethod
    def _addons_before_entry_points() -> list[type]:
        """The list as it was written here, for a venv whose packages predate the entry
        points — a release image built before they were published. Answered only
        when discovery finds nothing at all; to be deleted once every package below
        has been released with its `wex.addons` entry."""
        from wexample_wex_addon_ai.ai_addon_manager import AiAddonManager
        from wexample_wex_addon_app.app_addon_manager import AppAddonManager
        from wexample_wex_addon_dev_javascript.javascript_addon_manager import (
            JavascriptAddonManager,
        )
        from wexample_wex_addon_dev_php.php_addon_manager import PhpAddonManager
        from wexample_wex_addon_dev_python.python_addon_manager import (
            PythonAddonManager,
        )
        from wexample_wex_addon_filestate.filestate_addon_manager import (
            FilestateAddonManager,
        )
        from wexample_wex_addon_master.master_addon_manager import MasterAddonManager
        from wexample_wex_addon_package.package_addon_manager import (
            PackageAddonManager,
        )
        from wexample_wex_addon_process.process_addon_manager import (
            ProcessAddonManager,
        )
        from wexample_wex_addon_services_collab.services_collab_addon_manager import (
            ServicesCollabAddonManager,
        )
        from wexample_wex_addon_services_db.services_db_addon_manager import (
            ServicesDbAddonManager,
        )
        from wexample_wex_addon_services_monitoring.services_monitoring_addon_manager import (
            ServicesMonitoringAddonManager,
        )
        from wexample_wex_addon_services_platform.services_platform_addon_manager import (
            ServicesPlatformAddonManager,
        )
        from wexample_wex_core.addons.core.core_addon_manager import CoreAddonManager
        from wexample_wex_core.addons.demo.demo_addon_manager import DemoAddonManager
        from wexample_wex_core.addons.docker.docker_addon_manager import (
            DockerAddonManager,
        )
        from wexample_wex_core.addons.system.system_addon_manager import (
            SystemAddonManager,
        )

        return [
            AiAddonManager,
            AppAddonManager,
            PackageAddonManager,
            ProcessAddonManager,
            CoreAddonManager,
            DemoAddonManager,
            DockerAddonManager,
            MasterAddonManager,
            ServicesDbAddonManager,
            ServicesPlatformAddonManager,
            ServicesMonitoringAddonManager,
            ServicesCollabAddonManager,
            SystemAddonManager,
            FilestateAddonManager,
            JavascriptAddonManager,
            PhpAddonManager,
            PythonAddonManager,
        ]
