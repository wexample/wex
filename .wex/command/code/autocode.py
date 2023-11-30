import ast

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

        source = file_read(file_path)

        self.visit(ast.parse(source))

    def visit_FunctionDef(self, node):
        self.check_function(node)

    def visit_AsyncFunctionDef(self, node):
        self.check_function(node)

    def check_function(self, node):
        self.generic_visit(node)

        if not node.returns:
            if self.function_has_only_none_returns(node):
                print(self.file_path)

    def function_has_only_none_returns(self, node) -> bool:
        if any(not isinstance(return_node.value, (ast.NameConstant, type(None)))
               for return_node in ast.walk(node) if isinstance(return_node, ast.Return)):
            print(f"  Function '{node.name}' has non-empty return statements.")
            return False
        else:
            print(f"  Function '{node.name}' only has empty or 'None' return statements.")
            return True
