import os
import shutil

from addons.app.command.app.init import app__app__init


def create_test_app(kernel, name='test-app', services: [] = []) -> str:
    app_dir = kernel.path["tmp"] + 'tests/test-app/'
    test_dir = os.getcwd()

    kernel.log('Creating test app in : ' + app_dir)

    # Recreate test app dir.
    shutil.rmtree(app_dir, True)
    os.makedirs(app_dir)

    kernel.run_function(app__app__init, {
        'name': name,
        'app-dir': app_dir,
        'services': ','.join(services)
    })

    os.chdir(test_dir)

    return app_dir
