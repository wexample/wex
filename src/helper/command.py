import os
import re

from addons.app.const.app import APP_DIR_APP_DATA
from src.const.globals import (
    COMMAND_PATTERN_ADDON,
    COMMAND_PATTERN_APP,
    COMMAND_PATTERN_CORE,
    COMMAND_PATTERN_SERVICE,
    COMMAND_PATTERN_USER,
    COMMAND_TYPE_ADDON,
    COMMAND_TYPE_APP,
    COMMAND_TYPE_CORE,
    COMMAND_TYPE_SERVICE,
    COMMAND_TYPE_USER,
)


def build_command_match(command: str):
    match = re.match(COMMAND_PATTERN_ADDON, command)
    if match:
        return match, COMMAND_TYPE_ADDON

    match = re.match(COMMAND_PATTERN_SERVICE, command)
    if match:
        return match, COMMAND_TYPE_SERVICE

    match = re.match(COMMAND_PATTERN_APP, command)
    if match:
        return match, COMMAND_TYPE_APP

    match = re.match(COMMAND_PATTERN_USER, command)
    if match:
        return match, COMMAND_TYPE_USER

    match = re.match(COMMAND_PATTERN_CORE, command)
    if match:
        return match, COMMAND_TYPE_CORE

    return None, None


def build_command_path_from_match(kernel, match, command_type: str):
    if command_type == COMMAND_TYPE_ADDON:
        base_path = f"{kernel.path['addons']}{match.group(1)}/"
        return f"{base_path}command/{match.group(2)}/{match.group(3)}.py"
    elif command_type == COMMAND_TYPE_APP:
        return os.path.join(
            kernel.addons['app']['path']['call_app_dir'],
            APP_DIR_APP_DATA,
            'command',
            match[1],
            match[2] + '.py'
        )
    elif command_type == COMMAND_TYPE_SERVICE:
        return os.path.join(
            kernel.registry['services'][match[1]]['dir'],
            'command',
            match[2] + '.py'
        )
    elif command_type == COMMAND_TYPE_USER:
        return os.path.join(
            os.path.expanduser('~'),
            APP_DIR_APP_DATA,
            'command',
            match[1],
            match[2] + '.py'
        )

    return None

def execute_command(kernel, command, working_directory=None, stdout=None, stderr=None):
    # Performance optimisation
    import datetime
    import os
    import subprocess

    if working_directory is None:
        working_directory = os.getcwd()

    if stderr is None:
        stderr = subprocess.STDOUT

    date_now = datetime.date.today()
    date_formatted = date_now.strftime("%Y-%m-%d")

    # Create a log file with the timestamp in its name
    out_path = os.path.join(kernel.path['log'], f"{date_formatted}-{kernel.process_id}.out")
    err_path = os.path.join(kernel.path['log'], f"{date_formatted}-{kernel.process_id}.err")

    os.makedirs(
        kernel.path['log'],
        exist_ok=True
    )

    with open(out_path, 'w') as out_file:
        with open(err_path, 'w') as err_file:
            return subprocess.Popen(
                command,
                cwd=working_directory,
                stdout=stdout or out_file,
                stderr=stderr or err_file,
            )
