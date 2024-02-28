import hashlib
import json
import os
import shutil
from typing import TYPE_CHECKING, List, Optional, cast

from addons.app.command.app.init import app__app__init
from addons.app.command.env.get import _app__env__get, _app__has_env_var
from addons.app.const.app import APP_ENV_TEST
from addons.docker.helper.docker import docker_container_ip
from src.const.types import StringsList
from src.core.file.DirectoryStructure import DirectoryStructure

if TYPE_CHECKING:
    from src.core.Kernel import Kernel

DEFAULT_APP_TEST_NAME: str = "test-app"
DEFAULT_ENVIRONMENT_TEST_REMOTE: str = "test_remote"
DEFAULT_ENVIRONMENT_TEST_SERVER_USERNAME: str = "root"
DEFAULT_ENVIRONMENT_TEST_SERVER_PASSWORD: str = "TEST_PASSWORD"


def test_get_app_dir(kernel: "Kernel", name: str) -> str:
    apps_dir = cast(DirectoryStructure, kernel.system_root_directory.shortcuts["apps"])
    return (
        f"{os.path.join(apps_dir.get_parent_dir(), APP_ENV_TEST, name) + os.path.sep}"
    )


def test_build_app_name(
    name: str = DEFAULT_APP_TEST_NAME, services: Optional[StringsList] = None
) -> str:
    services = services or []

    data = {"name": name, "services": services}

    # Convert the dictionary to a JSON string
    data_str = json.dumps(data, sort_keys=True)

    # Create a hash object
    hash_object = hashlib.sha256()

    # Update the hash object with the bytes of the string
    hash_object.update(data_str.encode())

    # Get the hexadecimal representation of the digest
    return name + "-" + hash_object.hexdigest()[:8]


def test_create_app(
    kernel: "Kernel",
    name: str,
    services: Optional[List[str]] = None,
    force_restart: bool = False,
) -> str:
    app_dir = test_get_app_dir(kernel, name)
    current_dir = os.getcwd()

    # Recreate test app dir.
    if os.path.exists(app_dir):
        if not force_restart:
            return app_dir

        shutil.rmtree(app_dir)
    os.makedirs(app_dir)

    kernel.io.log("Creating test app in : " + app_dir)

    kernel.run_function(
        app__app__init,
        {
            "env": APP_ENV_TEST,
            "name": name,
            "app-dir": app_dir,
            "services": ",".join(services or []),
        },
    )

    os.chdir(current_dir)

    return app_dir


def test_get_test_remote_address(kernel: "Kernel") -> str:
    # A test remote container should have been started.
    return docker_container_ip(kernel, "wex_test_remote")
