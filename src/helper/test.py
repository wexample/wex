import os

from addons.core.command.registry.build import core__registry__build
from src.helper.command import build_function_name_from_match, build_command_path_from_match
from src.helper.file import create_from_template


def file_path_to_test_class_name(kernel, file_path: str) -> str:
    """
    Convert a file path to a test class name.

    Example: "addon/tests/command/group/name.py" becomes "TestAddonGroupName"
    """
    file_path = os.path.relpath(file_path, kernel.path['addons'])
    parts = file_path.split('/')
    parts = [p.capitalize() for p in parts]
    del parts[1]
    parts[-1] = f"{parts[-1][:-3]}"
    class_name = ''.join(parts)
    return f'Test{class_name}'


def file_path_to_test_method(kernel, file_path: str) -> str:
    """
    Convert a file path to a test method name.

    Example: "addon/tests/command/group/name.py"  becomes "test_name"
    """
    file_path = os.path.relpath(file_path, kernel.path['addons'])
    parts = file_path.split('/')
    file_name = parts[-1][:-3]
    test_method = f'test_{file_name}'
    return test_method


def create_test_from_command(kernel, command) -> str:
    match, command_type = kernel.build_match_or_fail(command)
    test_path = build_command_path_from_match(kernel, match, command_type, 'tests')

    if os.path.exists(test_path):
        return test_path

    class_name = file_path_to_test_class_name(kernel, test_path)
    method_name = file_path_to_test_method(kernel, test_path)
    command_function_name = build_function_name_from_match(match, command_type)

    kernel.log(f'Creating test for command {command}')

    kernel.log_indent_up()
    kernel.log(f'File : {test_path}')
    kernel.log(f'Class : {class_name}')
    kernel.log(f'Function : {method_name}')
    kernel.log_indent_down()

    create_from_template(
        kernel.path['templates'] + 'test.py.tpl',
        test_path,
        {
            'addon_name': match[1],
            'class_name': class_name,
            'command': command,
            'command_function_name': command_function_name,
            'group_name': match[2],
            'method_name': method_name,
            'name': match[3],
        }
    )

    kernel.exec_function(
        core__registry__build
    )

    kernel.message(f'Created test file : {test_path}')

    return test_path
