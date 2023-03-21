import subprocess


def shell_exec(command: str):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True
    )

    # Display output in real time.
    for line in iter(process.stdout.readline, b''):
        print(line.decode().strip())

    # Get output
    output, error = process.communicate()
    if error:
        print(error.decode())
    else:
        print(output.decode())
