import datetime
import os
import click

from src.const.globals import LOG_MAX_DAYS


@click.command
@click.pass_obj
def core_logs_rotate(kernel):
    # Define the age limit
    age_limit = datetime.timedelta(days=LOG_MAX_DAYS)
    # Get the current time
    now = datetime.datetime.now()
    # Get the list of log files
    log_files = os.listdir(kernel.path['logs'])

    kernel.log(f'Starting cleanup of files older than {LOG_MAX_DAYS} days')
    # Loop through the log files
    for log_file in log_files:
        # Get the full path to the log file
        log_file_path = os.path.join(kernel.path['logs'], log_file)
        # Get the modification time of the log file
        mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(log_file_path))

        # Check if the log file is older than the age limit
        if now - mod_time > age_limit:
            # If it is, delete the log file
            os.remove(log_file_path)

            kernel.log(f'Removed old log file : {log_file_path}')

