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
