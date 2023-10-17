from addons.app.const.app import APP_ENV_LOCAL, APP_ENV_PROD
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command
from addons.app.command.config.bind_files import app__config__bind_files
from addons.app.AppAddonManager import AppAddonManager


@command(help="Set configuration")
@app_dir_option()
@service_option()
def phpmyadmin__config__runtime(kernel: Kernel, app_dir: str, service: str):
    # Save config
    manager: AppAddonManager = kernel.addons['app']
    domain_pma = manager.get_runtime_config('domain_pma')

    if not domain_pma:
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

        print(domains)

        manager.set_runtime_config(
            'domains',
            domains
        )
