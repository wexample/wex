import yaml
import os

from yaml import SafeLoader

from addons.app.const.app import APP_DIR_APP_DATA, APP_FILE_APP_ENV, APP_FILEPATH_REL_CONFIG, PROXY_FILE_APPS_REGISTRY
from src.helper.file import create_directories_and_file
from src.helper.string import to_snake_case


def create_env(env, app_dir):
    create_directories_and_file(
        os.path.join(app_dir, APP_DIR_APP_DATA, APP_FILE_APP_ENV),
        f'APP_ENV={env}\n'
    )

    with open(os.path.join(app_dir, APP_DIR_APP_DATA, APP_FILE_APP_ENV), 'w') as f:
        f.write(f'APP_ENV={env}\n')


def set_app_workdir(kernel, app_dir):
    import yaml

    config_path = os.path.join(app_dir, APP_FILEPATH_REL_CONFIG)

    # Support invalid folders as work dir
    # might not be initialized at this point.
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            file_config = yaml.load(f, Loader=SafeLoader)
    else:
        file_config = {}

    kernel.addons['app']['call_command_level'] = 0

    kernel.addons['app']['config'] = {
        'context': {
            'call_working_dir': os.getcwd(),
            'dir': app_dir,
            'dir_wex': app_dir + APP_DIR_APP_DATA,
        },
        'path': {},
        'proxy': {
            'dir': kernel.addons['app']['path']['proxy']
        }
    }

    kernel.addons['app']['config'].update(file_config)

    os.chdir(app_dir)


def unset_app_workdir(kernel):
    # Restore previous working dir.
    os.chdir(kernel.addons['app']['config']['context']['call_working_dir'])

    del kernel.addons['app']['call_command_level']
    del kernel.addons['app']['config']['context']['call_working_dir']
    del kernel.addons['app']['config']['context']['dir']


def config_save(kernel):
    kernel.log('Updating app config...')

    with open(os.path.join(
            kernel.addons['app']['config']['context']['dir'],
            APP_FILEPATH_REL_CONFIG
    ), 'w') as f:
        yaml.dump(kernel.addons['app']['config'], f, indent=True)


def app_config_to_docker_env(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        new_key = to_snake_case(new_key)
        new_key = new_key.upper()
        if isinstance(v, dict):
            items.extend(app_config_to_docker_env(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def save_proxy_apps(kernel):
    with open(kernel.addons['app']['path']['proxy'] + PROXY_FILE_APPS_REGISTRY, 'w') as f:
        yaml.dump(
            kernel.addons['app']['proxy']['apps'], f,
            indent=True
        )


def is_app_root(app_dir: str) -> bool:
    if not os.path.exists(app_dir):
        return False

    # Search for config file.
    return os.path.exists(
        os.path.join(app_dir, APP_FILEPATH_REL_CONFIG)
    )
