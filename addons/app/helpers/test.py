import os
import shutil

from addons.app.command.app.init import app__app__init
from addons.app.command.app.start import app__app__start


def create_test_app(kernel, name='test-app', services: list | None = None, start: bool = False) -> str:
    app_dir = kernel.path["tmp"] + 'tests/test-app/'
    test_dir = os.getcwd()

    kernel.io.log('Creating test app in : ' + app_dir)

    # Recreate test app dir.
    shutil.rmtree(app_dir, True)
    os.makedirs(app_dir)

    kernel.run_function(app__app__init, {
        'name': name,
        'app-dir': app_dir,
        'services': ','.join(services or [])
    })

    os.chdir(test_dir)

    if start:
        kernel.run_function(
            app__app__start, {
                'app-dir': app_dir
            }
        )

    return app_dir
