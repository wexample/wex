import os
import yaml

from yaml import SafeLoader
from addons.app.const.app import APP_FILE_APP_SERVICE_CONFIG
from addons.app.command.env.get import app__env__get
from src.helper.registry import resolve_service_inheritance
from src.decorator.alias import alias
from src.decorator.command import command
from src.decorator.option import option
from src.decorator.as_sudo import as_sudo
from src.const.globals import FILE_REGISTRY, COMMAND_TYPE_ADDON, \
    COMMAND_TYPE_SERVICE
from src.helper.file import set_user_or_sudo_user_owner


@command(help="Rebuild core registry")
@as_sudo
@option('--test', '-t', is_flag=True, default=False,
        help="Register also commands marked as only for testing")
@option('--write', '-w', type=bool, default=True,
        help="Write registry file")
@alias('rebuild')
def core__registry__build(kernel, test: bool = False, write: bool = True):
    return _core__registry__build(kernel, test, write)


def _core__registry__build(kernel, test: bool = False, write: bool = True):
    kernel.io.log('Building registry...')
    addons = kernel.addons

    kernel.io.log_indent_up()

    # Call function avoiding core command management.
    env = app__env__get.callback.__wrapped__(
        kernel,
        kernel.get_path('root')
    )

    registry = {
        COMMAND_TYPE_ADDON: build_registry_addons(addons, kernel, test),
        COMMAND_TYPE_SERVICE: build_registry_services(addons, kernel, test),
        'env': env,
    }

    kernel.io.log('Building complete...')
    kernel.io.log_indent_down()

    if write:
        registry_path = os.path.join(kernel.get_or_create_path('tmp'), FILE_REGISTRY)
        with open(registry_path, 'w') as f:
            yaml.dump(registry, f)

        set_user_or_sudo_user_owner(registry_path)
        kernel.load_registry()
    else:
        return registry


def build_registry_addons(addons, kernel, test_commands: bool = False):
    addons_dict = {}
    resolver = kernel.get_command_resolver(COMMAND_TYPE_ADDON)

    for addon in addons:
        addon_command_path = os.path.join(kernel.get_path('addons'), addon, 'command')

        if os.path.exists(addon_command_path):
            addons_dict[addon] = {
                'name': addon,
                'commands': resolver.scan_commands_groups(
                    addon_command_path,
                    test_commands
                )
            }

    return addons_dict


def build_registry_services(addons, kernel, test_commands: bool = False):
    services_dict = {}
    resolver = kernel.get_command_resolver(COMMAND_TYPE_SERVICE)

    for addon in addons:
        services_dir = os.path.join(kernel.get_path('addons'), addon, 'services')
        if os.path.exists(services_dir):
            for service in os.listdir(services_dir):
                kernel.io.log(f'Found service {service}')
                service_path = os.path.join(services_dir, service)
                config_file_path = os.path.join(service_path, APP_FILE_APP_SERVICE_CONFIG)
                commands_path = os.path.join(service_path, 'command')

                services_dict[service] = {
                    'name': service,
                    'commands': resolver.scan_commands_groups(
                        commands_path,
                        test_commands
                    ),
                    'addon': addon,
                    'dir': service_path + '/',
                    "config": (yaml.load(
                        open(config_file_path),
                        SafeLoader
                    ) or {}) if os.path.exists(config_file_path) else {
                        'dependencies': []
                    }
                }

    # Resolve inheritance
    for service_name, service_data in services_dict.items():
        resolve_service_inheritance(service_data, services_dict)

    return services_dict
