import os
import shutil

from addons.app.command.app.init import app__app__init
from addons.app.const.app import APP_ENV_TEST


def create_test_app_dir(kernel, name: str | None = None) -> str:
    return f'{kernel.path["tmp"]}tests/{name or "test-app"}/'


def create_test_app(kernel, name: str | None = None, services: list | None = None) -> str:
    name = name or 'test-app'
    app_dir = create_test_app_dir(kernel, name)
    test_dir = os.getcwd()

    kernel.io.log('Creating test app in : ' + app_dir)

    # Recreate test app dir.
    shutil.rmtree(app_dir)
    os.makedirs(app_dir)

    kernel.run_function(app__app__init, {
        'env': APP_ENV_TEST,
        'name': name,
        'app-dir': app_dir,
        'services': ','.join(services or [])
    })

    os.chdir(test_dir)

    return app_dir
