import ast
import re

from addons.app.AppAddonManager import AppAddonManager
from src.helper.file import file_search, file_read
from src.const.globals import COMMAND_TYPE_APP
from addons.app.decorator.app_command import app_command


@app_command(help="An app test command", command_type=COMMAND_TYPE_APP)
def app__code__autocode(manager: AppAddonManager, app_dir: str) -> None:
    explore_and_modify_files(manager, manager.kernel.directory.path + 'addons/')


def explore_and_modify_files(manager: AppAddonManager, directory: str) -> None:
    manager.kernel.io.log('Searching directory ' + directory)

    files = file_search(directory, '.py')

    for file_path in files:
        FunctionMethodVisitor(file_path)


class FunctionMethodVisitor(ast.NodeVisitor):
    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self._source = file_read(file_path)
        self.visit(ast.parse(self._source))

    def visit_FunctionDef(self, node):
        self.check_function(node)

    def visit_AsyncFunctionDef(self, node):
        self.check_function(node)

    def check_function(self, node):
        self.generic_visit(node)

        if not node.returns:
            if self.function_has_only_none_returns(node):
                print(f"  Function '{node.name}' has been modified")
                print(self.file_path)

                # Append ' -> None' to function definition
                self._source = re.sub(rf"def {node.name}\(([^)]*)\):", rf"def {node.name}(\1) -> None:", self._source)

                # Write the changes back to the file
                with open(self.file_path, "w") as file:
                    file.write(self._source)

    def function_has_only_none_returns(self, node) -> bool:
        return all(isinstance(return_node.value, (ast.NameConstant, type(None)))
                   for return_node in ast.walk(node) if isinstance(return_node, ast.Return))
