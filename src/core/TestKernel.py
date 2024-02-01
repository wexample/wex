import os

from addons.docker.helper.docker import docker_container_ip
from src.const.globals import VERBOSITY_LEVEL_MAXIMUM
from src.core.Kernel import Kernel


class TestKernel(Kernel):
    # Post-exec script should be tested with
    # dedicated subprocesses during tests
    fast_mode = True
    verbosity: int = VERBOSITY_LEVEL_MAXIMUM
    tty = False

    def __init__(self, entrypoint_path: str, task_id: str | None = None) -> None:
        super().__init__(
            entrypoint_path,
            task_id,
        )

        remote_address = os.environ.get("TEST_REMOTE_ADDRESS")
        if not remote_address:
            # A test remote container should have been started.
            self.remote_address = docker_container_ip(self, "wex_test_remote")
        else:
            self.remote_address = str(remote_address)
