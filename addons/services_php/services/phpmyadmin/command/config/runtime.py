from addons.app.const.app import APP_ENV_LOCAL, APP_ENV_PROD
from addons.app.AppAddonManager import AppAddonManager
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Set runtime configuration", command_type=COMMAND_TYPE_SERVICE)
def phpmyadmin__config__runtime(kernel: 'Kernel', app_dir: str, service: str):
    # Save config
    manager: AppAddonManager = kernel.addons['app']
    domain_pma = manager.get_runtime_config('domain_pma', None)

    # Setting false to domain will disable domain setting,
    # used to disable phpmyadmin in some environment.
    if domain_pma is not False:
        if domain_pma is None:
            env = manager.get_runtime_config('env')

            domain_pma = ['pma']
            if env != APP_ENV_LOCAL and env != APP_ENV_PROD:
                domain_pma.append(env)

            domain_pma.append(
                manager.get_runtime_config('domain_tld')
            )

            domain_pma = '.'.join(domain_pma)

            manager.set_runtime_config(
                'domain_pma',
                domain_pma
            )

        domains = manager.get_runtime_config(
            'domains',
            []
        )

        domains.append(domain_pma)

        manager.set_runtime_config(
            'domains',
            domains
        )
