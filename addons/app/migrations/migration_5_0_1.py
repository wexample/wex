from src.helper.prompt import prompt_progress_steps
from addons.app.const.app import APP_DIR_APP_DATA, APP_FILE_APP_CONFIG
from addons.app.AppAddonManager import AppAddonManager
from addons.app.migrations.migration_4_0_0 import _migration_4_0_0_replace_docker_mapping, \
    _migration_4_0_0_replace_placeholders, _migration_4_0_0_replace_docker_placeholders
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


def migration_5_0_1(kernel: 'Kernel', manager: AppAddonManager):
    env_dir = f'{manager.app_dir}{APP_DIR_APP_DATA}'

    def _migration_5_0_1_update_config():
        mapping = {
            # The only cli known was wordpress_cli
            '_mysql_8': '_mysql',
            ' mysql_8': ' mysql',
            ' php_8': ' php',
        }

        _migration_4_0_0_replace_docker_mapping(manager, mapping)

        _migration_4_0_0_replace_placeholders(
            env_dir + APP_FILE_APP_CONFIG,
            mapping
        )

        _migration_4_0_0_replace_docker_placeholders(manager, {
            "RUNTIME_SERVICE_MYSQL_8_YML_ENV": "RUNTIME_SERVICE_MYSQL_YML_ENV",
            "RUNTIME_SERVICE_PHP_8_YML_ENV": "RUNTIME_SERVICE_PHP_YML_ENV",
            "RUNTIME_PATH_APP_WEX": "RUNTIME_PATH_APP_ENV",
        })

        manager.load_config()
        manager.set_config('global.type', 'app')

    prompt_progress_steps(kernel, [
        _migration_5_0_1_update_config,
    ])
