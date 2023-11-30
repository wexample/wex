import ast
import os
import re

from addons.app.AppAddonManager import AppAddonManager
from src.helper.file import file_search, file_read
from src.const.globals import COMMAND_TYPE_APP
from addons.app.decorator.app_command import app_command


@app_command(help="An app test command", command_type=COMMAND_TYPE_APP)
def app__code__autocode(manager: AppAddonManager, app_dir: str) -> None:
    python_dirs = [
        'addons',
        'src',
        'tests',
    ]

    for dir in python_dirs:
        explore_and_modify_files(
            manager,
            os.path.join(manager.kernel.directory.path, dir) + os.sep)


def explore_and_modify_files(manager: AppAddonManager, directory: str) -> None:
    manager.kernel.io.log('Searching directory ' + directory)

    files = file_search(directory, '.py')

    for file_path in files:
        FunctionMethodVisitor(file_path)


class FunctionMethodVisitor(ast.NodeVisitor):
    def __init__(self, file_path: str) -> None:
        self._file_path: str = file_path
        self._source = file_read(file_path)
        self._node = ast.parse(self._source)

        self.visit(self._node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.check_function(node)

    def visit_AsyncFunctionDef(self, node: ast.FunctionDef) -> None:
        self.check_function(node)

    def check_function(self, node: ast.FunctionDef) -> None:
        self.generic_visit(node)

        # Add missing "-> None" to functions
        if not node.returns and self.function_has_only_none_returns(node):
            self._source = re.sub(rf"def {node.name}\(([^)]*)\):", rf"def {node.name}(\1) -> None:", self._source)

        # When an argument of a function is called "kernel", add "Kernel" as type
        self._source = self.add_kernel_annotation(self._source, node.name)

        # Write the changes back to the file
        with open(self._file_path, "w") as file:
            file.write(self._source)

    def add_kernel_annotation(self, source_code: str, function_name: str) -> str:
        pattern = rf"def {function_name}\((.*?)\)"
        matches = re.finditer(pattern, source_code, re.DOTALL)

        for match in matches:
            args_string = match.group(1)
            args = [arg.strip() for arg in args_string.split(',')]
            new_args = []
            kernel_modified = False
            for arg in args:
                if "kernel" in arg and ":" not in arg:
                    arg = 'kernel: "Kernel"'
                    kernel_modified = True
                new_args.append(arg)
            if kernel_modified:
                self.log_modified()
                new_args_string = ', '.join(new_args)
                source_code = re.sub(pattern, rf'def {function_name}({new_args_string})', source_code, count=1)

        return source_code

    def log_modified(self):
        print(f"  Function '{self._node.name}' has been modified")
        print(self._file_path)


    def function_has_only_none_returns(self, node: ast.FunctionDef) -> bool:
        return all(isinstance(return_node.value, (ast.NameConstant, type(None)))
                   for return_node in ast.walk(node) if isinstance(return_node, ast.Return))
