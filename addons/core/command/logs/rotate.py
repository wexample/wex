import datetime
import os
from typing import List

from src.decorator.option import option
from src.decorator.command import command
from src.core import Kernel


@command(help="Remove old logs files")
@option('--max-days', '-md', required=False, default=10)
def core__logs__rotate(kernel: Kernel, max_days: int = 10):
    """
    Rotate and clean up log files older than a specified age limit.

    This function iterates through the log files in the 'log' directory, checks their modification
    time, and removes any log files that are older than the age limit defined by LOG_MAX_DAYS.
    """
    # Define the age limit
    age_limit: datetime.timedelta = datetime.timedelta(days=max_days)
    # Get the current time
    now: datetime.datetime = datetime.datetime.now()
    # Get the list of log files
    log_files: List[str] = os.listdir(kernel.path['log'])

    kernel.log(f'Starting cleanup of files older than {max_days} days')
    # Loop through the log files
    for log_file in log_files:
        log_file_path: str = os.path.join(kernel.path['log'], log_file)
        # Get the modification time of the log file
        mod_time: datetime.datetime = datetime.datetime.fromtimestamp(os.path.getmtime(log_file_path))

        # Check if the log file is older than the age limit
        if now - mod_time > age_limit:
            # If it is, delete the log file
            os.remove(log_file_path)

            kernel.log(f'Removed old log file : {log_file_path}')
