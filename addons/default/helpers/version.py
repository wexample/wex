import importlib
import os

from src.const.error import ERR_UNEXPECTED
from src.core.response.AbortResponse import AbortResponse
from src.core.Kernel import Kernel


def is_greater_than(first, second, true_if_equal=False):
    keys_to_check = [
        'major',
        'intermediate',
        'minor',
        'pre_build_type',
        'pre_build_number'
    ]

    for key in keys_to_check:
        first_value = first.get(key, None)
        second_value = second.get(key, None)

        if first_value is None and second_value is not None:
            return False
        elif first_value is not None and second_value is None:
            return True

        if first_value is not None and second_value is not None:
            if first_value < second_value:
                return False
            elif first_value > second_value:
                return True

    return true_if_equal


def version_join(version: dict, add_build: bool = False) -> str:
    output = f"{version['major']}.{version['intermediate']}.{version['minor']}"

    # Build version string
    version['pre_build_info'] = ''
    if version['pre_build_type']:
        output += f'-{version["pre_build_type"]}.{version["pre_build_number"]}'

    if add_build:
        import datetime
        output += f'+build.' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    return output


def version_exec(kernel: Kernel, version: str, method_part: str):
    version_snake = version.replace(".", "_")
    path_migrations = os.path.join(kernel.path['addons'], 'app/migrations') + os.sep
    method_name = f"{method_part}_{version_snake}"

    # Dynamically import the module
    module_name = version.replace(".py", "")

    spec = importlib.util.spec_from_file_location(module_name, path_migrations + version + '.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Get the method from the module
    method_to_call = getattr(module, method_name, None)

    if method_to_call is None:
        import logging
        kernel.error(
            ERR_UNEXPECTED,
            {
                'error': f"Method {method_name} not found in module {module_name}"
            },
            logging.ERROR
        )

        return AbortResponse(kernel)

    # Execute the method
    method_to_call(kernel)
