import os.path

from src.core import Kernel
from addons.app.AppAddonManager import AppAddonManager


def migration_5_0_0(kernel: Kernel, manager: AppAddonManager):
    config = _parse_4_0_0_config_file(manager.app_dir + '.wex/config')

    if config:
        for domain_env_name in ['LOCAL', 'DEV', 'PROD']:
            env_name = domain_env_name.lower()
            manager.config['env'][env_name]['domains'] = _get_config_value(config, domain_env_name + '_DOMAINS')
            manager.config['env'][env_name]['domain_main'] = _get_config_value(config, domain_env_name + '_DOMAIN_MAIN')
            manager.config['env'][env_name]['email'] = _get_config_value(config, domain_env_name + '_EMAIL', 'contact@domain.com')

        manager.config['global']['name'] = _get_config_value(config, 'NAME', manager.get_config('global.config', 'undefined'))
        manager.config['global']['services'] = _get_config_value(config, 'SERVICES', [])


def is_version_5_0_0(kernel: Kernel, path: str):
    # Not implemented yet.
    return None


def _get_config_value(config: dict, key: str, default=None):
    return config[key] if key in config else default


def _parse_4_0_0_config_file(file_path: str):
    if not os.path.isfile(file_path):
        return None

    config = {}

    with open(file_path, 'r') as f:
        for line in f.readlines():
            # Ignoring comments and empty lines
            line = line.strip()
            if line.startswith("#") or not line:
                continue

            key, value = line.split("=", 1)

            # If the value contains commas, convert it to a list
            if ',' in value:
                value = value.split(',')

            config[key] = value

    return config
