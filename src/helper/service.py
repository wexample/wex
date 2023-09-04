import os


def get_service_dir(kernel, service: str) -> str:
    addon = kernel.registry['services'][service]['addon']

    return os.path.join(kernel.path['addons'], addon, 'services', service)
