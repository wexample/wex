import re

from addons.app.AppAddonManager import AppAddonManager
from src.const.globals import COMMAND_TYPE_APP
from addons.app.decorator.app_command import app_command
import os


@app_command(help="An app test command", command_type=COMMAND_TYPE_APP)
def app__code__autocode(manager: AppAddonManager, app_dir: str) -> None:
    explore_and_modify_files(manager, manager.kernel.directory.path + 'addons/')


def explore_and_modify_files(manager: AppAddonManager, directory: str) -> None:
    manager.kernel.io.log('Searching directory ' + directory)

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    contents = f.readlines()

                # Inside each found file.
                manager.kernel.io.log('Working on ' + file_path)

                modified_contents = []
                changed = False
                for line in contents:
                    test_function_pattern = re.compile(r"(  +)def test_(.*?)\((.*?)\):")

                    if test_function_pattern.match(line) and "-> None" not in line:
                        line = test_function_pattern.sub(r"\1def test_\2(\3) -> None:", line)
                        changed = True
                    modified_contents.append(line)

                if changed:
                    manager.kernel.io.print('Changed : ' + file_path)

                #     with open(file_path, "w") as f:
                #         f.writelines(modified_contents)
