import subprocess
import datetime
import os


def command_exists(command) -> bool:
    process = subprocess.Popen(
        'command -v ' + command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    out_content, err_content = process.communicate()

    return out_content.decode() != ''


def prepare_logs(kernel):
    date_now = datetime.date.today()
    date_formatted = date_now.strftime("%Y-%m-%d")

    os.makedirs(kernel.path['log'], exist_ok=True)

    out_path = os.path.join(kernel.path['log'], f"{date_formatted}-{kernel.task_id}.out")
    err_path = os.path.join(kernel.path['log'], f"{date_formatted}-{kernel.task_id}.err")

    return out_path, err_path


def execute_command(kernel, command, working_directory=None, async_mode=False):
    if working_directory is None:
        working_directory = os.getcwd()

    out_path, err_path = prepare_logs(kernel)

    process = subprocess.Popen(
        command,
        cwd=working_directory,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if async_mode:
        # Just return the process object, and the caller can decide what to do with it.
        return process
    else:
        out_content, err_content = process.communicate()
        success = (process.returncode == 0)

        # Log stdout and stderr
        with open(out_path, 'a') as out_file:
            out_file.write(out_content.decode())
        with open(err_path, 'a') as err_file:
            err_file.write(err_content.decode())

        return success, out_content.decode().splitlines() if success else err_content.decode().splitlines()


def command_to_string(command):
    output = []

    for item in command:
        if isinstance(item, list):
            output.append(
                '$(' + command_to_string(item) + ')'
            )
        else:
            output.append('"' + item + '"' if ' ' in item else item)

    return ' '.join(output)
