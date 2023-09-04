
import os
import re

from src.core import Kernel
from src.helper.string import to_snake_case, to_pascal_case
from src.helper.file import create_from_template


def file_path_to_test_class_name(kernel, file_path: str) -> str:
    """
    Convert a file path to a test class name.

    Example: "addon/tests/command/group/name.py" becomes "TestAddonGroupName"
    """
    file_path = os.path.relpath(file_path, kernel.path['addons'])
    parts = file_path.split('/')

    # Remove the file extension from the last part
    parts[-1] = os.path.splitext(parts[-1])[0]

    parts = [to_pascal_case(re.sub(r'[-_]', ' ', p)) for p in parts]

    del parts[1]
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


def create_test_from_command(kernel: Kernel, command: str, force: bool = False) -> str:
    request = kernel.create_command_request(command)
    test_path = request.resolver.build_path_or_fail(request, 'tests')

    # File exists
    if os.path.exists(test_path) and not force:
        return test_path

    class_name = file_path_to_test_class_name(kernel, test_path)
    method_name = file_path_to_test_method(kernel, test_path)
    command_function_name = request.resolver.get_function_name(
        list(request.match.groups())
    )

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
            'addon_name': request.match[1],
            'class_name': class_name,
            'command': command,
            'command_function_name': command_function_name,
            'dir_group': to_snake_case(request.match[2]),
            'dir_name': to_snake_case(request.match[3]),
            'group_name': request.match[2],
            'method_name': method_name,
            'name': request.match[3],
        }
    )

    kernel.rebuild()

    kernel.message(f'Created test file : {test_path}')

    return test_path
