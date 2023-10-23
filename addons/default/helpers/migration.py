import importlib
import os
import re

from src.core.Kernel import Kernel

MIGRATION_MINIMAL_VERSION = '3.0.0'


def get_migrations_path(kernel: Kernel) -> str:
    return os.path.join(kernel.path['addons'], 'app/migrations') + os.sep


def get_migrations_files(kernel: Kernel):
    migrations_path = get_migrations_path(kernel)

    # List .py files in the migrations path
    py_files = [f for f in os.listdir(migrations_path)
                if os.path.isfile(os.path.join(migrations_path, f)) and f.endswith('.py')]

    # Sort the list of files based on the version numbers
    sorted_py_files = sorted(py_files, key=lambda f: tuple(map(int, re.findall(r'\d+', f))))

    return sorted_py_files


def migration_get_function(kernel: Kernel, version: str, method_part: str):
    version_snake = version.replace(".", "_")
    path_migrations = get_migrations_path(kernel)
    method_name = f"{method_part}_{version_snake}"

    spec = importlib.util.spec_from_file_location('migration_' + version_snake, path_migrations + 'migration_' + version_snake + '.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Get the method from the module
    return getattr(module, method_name, None)


def migration_exec(kernel: Kernel, version: str, method_part: str, arguments: []):
    function = migration_get_function(
        kernel,
        version,
        method_part
    )

    if function:
        return function(*([kernel] + arguments))

    return None


def version_guess(kernel: Kernel, path: str):
    for migration_file in get_migrations_files(kernel):
        version_string = migration_file.replace(".py", "")
        version_string = version_string.replace("migration_", "")

        result = migration_exec(
            kernel,
            version_string,
            'is_version',
            [path]
        )

        if result:
            return version_string.replace('_', '.')

    return MIGRATION_MINIMAL_VERSION


def migration_delete_dir_if_empty(kernel: Kernel, target_dir: str):
    if not os.path.exists(target_dir):
        kernel.io.log(f'Dir already deleted : {target_dir}')
    elif len(os.listdir(target_dir)):
        kernel.io.log(f'Dir not empty, leaving as it is : {target_dir}')
    else:
        os.rmdir(target_dir)


def extract_version_from_file_name(filename: str) -> None | str:
    match = re.search(r'migration_(\d+_\d+_\d+)\.py', filename)
    if match:
        version = match.group(1).replace('_', '.')
        return version
    return None
