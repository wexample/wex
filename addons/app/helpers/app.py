import yaml
import os

from addons.app.const.app import APP_DIR_APP_DATA, APP_FILE_APP_ENV, APP_FILEPATH_REL_CONFIG, PROXY_FILE_APPS_REGISTRY, \
    APP_FILEPATH_REL_CONFIG_BUILD, APP_FILEPATH_REL_DOCKER_ENV
from src.const.globals import COLOR_GRAY
from src.helper.file import create_directories_and_file, yaml_load_or_default, get_dict_item_by_path, \
    write_dict_to_config
from src.helper.string import to_snake_case


def create_env(env, app_dir):
    create_directories_and_file(
        os.path.join(app_dir, APP_DIR_APP_DATA, APP_FILE_APP_ENV),
        f'APP_ENV={env}\n'
    )

    with open(os.path.join(app_dir, APP_DIR_APP_DATA, APP_FILE_APP_ENV), 'w') as f:
        f.write(f'APP_ENV={env}\n')


def set_app_workdir(kernel, app_dir):
    config_path = os.path.join(app_dir, APP_FILEPATH_REL_CONFIG)
    file_config = yaml_load_or_default(config_path)

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

    # Load build config if app started
    kernel.addons['app']['config_build'] = yaml_load_or_default(
        os.path.join(
            app_dir,
            APP_FILEPATH_REL_CONFIG_BUILD
        ),
        {
            'context': {
                'started': False
            }
        }
    )

    os.chdir(app_dir)


def unset_app_workdir(kernel):
    # Restore previous working dir.
    os.chdir(kernel.addons['app']['config']['context']['call_working_dir'])

    del kernel.addons['app']['call_command_level']
    del kernel.addons['app']['config']['context']['call_working_dir']
    del kernel.addons['app']['config']['context']['dir']


def config_save(kernel, key: str = 'config', config_path: str = APP_FILEPATH_REL_CONFIG, app_dir: str = None):
    app_log(kernel, 'Updating app config...')

    if app_dir is None:
        app_dir = kernel.addons['app']['config']['context']['dir']

    if config_path is None:
        config_path = os.path.join(
            app_dir,
            APP_FILEPATH_REL_CONFIG
        )

    with open(config_path, 'w') as f:
        yaml.dump(kernel.addons['app'][key], f, indent=True)


def config_save_build(kernel, app_dir: str = None):
    config_save(
        kernel,
        'config_build',
        APP_FILEPATH_REL_CONFIG_BUILD,
        app_dir
    )

    # Write as docker env file
    write_dict_to_config(
        app_config_to_docker_env(
            dict(
                sorted(
                    kernel.addons['app']['config_build'].items()
                )
            )
        ),
        APP_FILEPATH_REL_DOCKER_ENV
    )


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


def app_exec_in_workdir(kernel, app_dir: str, callback):
    kernel.log_indent_up()
    app_dir_previous = os.getcwd() + '/'
    set_app_workdir(kernel, app_dir)

    response = callback()

    set_app_workdir(kernel, app_dir_previous)
    kernel.log_indent_down()

    return response


def app_log(kernel, message: str, color=COLOR_GRAY, increment: int = 0) -> None:
    return kernel.log(
        f'[{get_dict_item_by_path(kernel.addons["app"]["config"], "global.name")}] {message}',
        color,
        increment + 1
    )
