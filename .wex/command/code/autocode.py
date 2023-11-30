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
        visitor = FunctionMethodVisitor()
        visitor.parse_file(file_path)


class FunctionMethodVisitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        self.check_function(node)

    def visit_AsyncFunctionDef(self, node):
        self.check_function(node)

    def parse_file(self, file_path: str):
        source = file_read(file_path)

        self.visit(
            ast.parse(source)
        )

    def check_function(self, node):
        print(f"Async function found: {node.name}")
        self.generic_visit(node)


def parse_functions_from_file(file_path):
    with open(file_path, "r") as source:
        tree = ast.parse(source.read())
        visitor = FunctionMethodVisitor()
        visitor.visit(tree)
