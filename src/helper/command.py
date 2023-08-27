import subprocess
import datetime
import os


def execute_command(kernel, command, working_directory=None) -> list[str]:
    if working_directory is None:
        working_directory = os.getcwd()

    date_now = datetime.date.today()
    date_formatted = date_now.strftime("%Y-%m-%d")

    # Create a log file with the timestamp in its name
    out_path = os.path.join(kernel.path['log'], f"{date_formatted}-{kernel.process_id}.out")
    err_path = os.path.join(kernel.path['log'], f"{date_formatted}-{kernel.process_id}.err")

    os.makedirs(
        kernel.path['log'],
        exist_ok=True
    )

    process = subprocess.Popen(
        command,
        cwd=working_directory,
        stdout=subprocess.PIPE,  # We'll capture stdout here
        stderr=subprocess.PIPE,  # ... and stderr here
    )

    out_content, err_content = process.communicate()

    # Now, we'll write the captured stdout and stderr to the log files
    with open(out_path, 'w') as out_file:
        out_file.write(out_content.decode())

    with open(err_path, 'w') as err_file:
        err_file.write(err_content.decode())

    return (out_content.decode().splitlines()
            + err_content.decode().splitlines())


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
