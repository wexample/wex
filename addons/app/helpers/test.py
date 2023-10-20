import hashlib
import json
import os
import shutil

from addons.app.command.app.init import app__app__init
from addons.app.const.app import APP_ENV_TEST

DEFAULT_APP_TEST_NAME: str = 'test-app'


def get_test_app_dir(kernel, name: str) -> str:
    return f'{kernel.path["tmp"]}tests/{name}/'


def build_test_app_name(
        name: str = DEFAULT_APP_TEST_NAME,
        services: list = None):
    services = services or []

    data = {
        'name': name,
        'services': services
    }

    # Convert the dictionary to a JSON string
    data_str = json.dumps(data, sort_keys=True)

    # Create a hash object
    hash_object = hashlib.sha256()

    # Update the hash object with the bytes of the string
    hash_object.update(data_str.encode())

    # Get the hexadecimal representation of the digest
    return name + '-' + hash_object.hexdigest()[:8]


def create_test_app(
        kernel,
        name: str,
        services: list | None = None,
        force_restart: bool = False) -> str:
    app_dir = get_test_app_dir(kernel, name)
    test_dir = os.getcwd()

    # Recreate test app dir.
    if os.path.exists(app_dir):
        if not force_restart:
            return app_dir

        shutil.rmtree(app_dir)
    os.makedirs(app_dir)

    kernel.io.log('Creating test app in : ' + app_dir)

    kernel.run_function(app__app__init, {
        'env': APP_ENV_TEST,
        'name': name,
        'app-dir': app_dir,
        'services': ','.join(services or [])
    })

    os.chdir(test_dir)

    return app_dir
