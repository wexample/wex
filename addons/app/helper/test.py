import hashlib
import json
import os
import shutil
from typing import TYPE_CHECKING, List, Optional

from addons.app.command.app.init import app__app__init
from addons.app.const.app import APP_ENV_TEST
from src.const.types import StringsList

if TYPE_CHECKING:
    from src.core.Kernel import Kernel

DEFAULT_APP_TEST_NAME: str = "test-app"


def test_get_app_dir(kernel: "Kernel", name: str) -> str:
    return f"{kernel.get_or_create_path('tmp')}tests/{name}/"


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
    test_dir = os.getcwd()

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

    os.chdir(test_dir)

    return app_dir
