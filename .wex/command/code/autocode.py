import ast
import os
import re

from addons.app.AppAddonManager import AppAddonManager
from const.types import AnyCallable
from src.helper.file import file_search, file_read
from src.const.globals import COMMAND_TYPE_APP
from addons.app.decorator.app_command import app_command


@app_command(help="An app test command", command_type=COMMAND_TYPE_APP)
def app__code__autocode(manager: AppAddonManager, app_dir: str) -> None:
    python_dirs = [
        '.wex/command',
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

        self.visit(ast.parse(self._source))

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.check_function(node)

    def visit_AsyncFunctionDef(self, node: ast.FunctionDef) -> None:
        self.check_function(node)

    def check_function(self, node: ast.FunctionDef) -> None:
        self.generic_visit(node)

        # Add missing "-> None" to functions
        if not node.returns:
            if self.function_has_only_none_returns(node):
                self._source = re.sub(rf"def {node.name}\(([^)]*)\)( -> [^:]+)?:", rf"def {node.name}(\1) -> None:",
                                      self._source)
                self.log_modified(node)
            elif self.function_has_only_bool_returns(node):
                self._source = re.sub(rf"def {node.name}\(([^)]*)\)( -> [^:]+)?:", rf"def {node.name}(\1) -> bool:",
                                      self._source)
                self.log_modified(node)
            elif self.function_has_only_string_returns(node):
                self._source = re.sub(rf"def {node.name}\(([^)]*)\)( -> [^:]+)?:", rf"def {node.name}(\1) -> str:",
                                      self._source)
                self.log_modified(node)
            elif self.function_has_only_int_returns(node):
                self._source = re.sub(rf"def {node.name}\(([^)]*)\)( -> [^:]+)?:", rf"def {node.name}(\1) -> int:",
                                      self._source)
                self.log_modified(node)

        # When an argument of a function is called "kernel", add "Kernel" as type
        self._source = self.add_kernel_annotation(self._source, node)

        # Write the changes back to the file
        with open(self._file_path, "w") as file:
            file.write(self._source)

    def add_kernel_annotation(self, source_code: str, node: ast.FunctionDef) -> str:
        pattern = rf"def {node.name}\((.*?)\)"
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
                self.log_modified(node)
                new_args_string = ', '.join(new_args)
                source_code = re.sub(pattern, rf'def {node.name}({new_args_string})', source_code, count=1)

        return source_code

    def function_returns_only_specific_type(self, node: ast.FunctionDef, type_check_function: AnyCallable) -> bool:
        for return_node in ast.walk(node):
            if isinstance(return_node, ast.Return):
                if not type_check_function(return_node):
                    return False
        return True

    def log_modified(self, node: ast.FunctionDef) -> None:
        print(f"  Function '{node.name}' has been modified")
        print(self._file_path)

    def function_has_only_none_returns(self, node: ast.FunctionDef) -> bool:
        return self.function_returns_only_specific_type(node, self.is_none_return)

    def function_has_only_bool_returns(self, node: ast.FunctionDef) -> bool:
        return self.function_returns_only_specific_type(node, self.is_bool_return)

    def function_has_only_string_returns(self, node: ast.FunctionDef) -> bool:
        return self.function_returns_only_specific_type(node, self.is_string_return)

    def function_has_only_int_returns(self, node: ast.FunctionDef) -> bool:
        return self.function_returns_only_specific_type(node, self.is_int_return)

    def is_none_return(self, return_node: ast.Return) -> bool:
        return return_node.value is None or \
            (isinstance(return_node.value, ast.NameConstant) and return_node.value.value is None)

    def is_bool_return(self, return_node: ast.Return) -> bool:
        return isinstance(return_node.value, ast.NameConstant) and isinstance(return_node.value.value, bool)

    def is_string_return(self, return_node: ast.Return) -> bool:
        return isinstance(return_node.value, ast.Str)

    def is_int_return(self, return_node: ast.Return) -> bool:
        return isinstance(return_node.value, ast.Num) and isinstance(return_node.value.n, int)
