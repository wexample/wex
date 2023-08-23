import os
import shutil

from addons.app.command.app.init import app__app__init


def create_test_app(kernel, name='test-app', services: [] = []):
    kernel.log('Creating test app...')

    app_dir = kernel.path["tmp"] + 'tests/test-app/'

    # Recreate test app dir.
    shutil.rmtree(app_dir, True)
    os.makedirs(app_dir)

    kernel.exec_function(app__app__init, {
        'name': name,
        'app-dir': app_dir,
        'services': ','.join(services)
    })
