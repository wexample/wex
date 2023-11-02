import datetime
import json
import os
import time

from src.helper.file import set_user_or_sudo_user_owner
from src.helper.json import load_json_if_valid
from src.const.globals import COMMAND_TYPE_ADDON

LOG_STATUS_COMPLETE = 'complete'
LOG_STATUS_STARTED = 'started'


class Logger:
    current_command = None

    def __init__(self, kernel):
        self.kernel = kernel

        log_dir = self.kernel.get_or_create_path('log')

        self.path_log = os.path.join(
            log_dir,
            kernel.task_id + '.json'
        )
        self.path_output = os.path.join(
            log_dir,
            f'{kernel.task_id}.out'
        )

        self.time_start = time.time()
        date_now = self.get_time_string()

        self.log_data = load_json_if_valid(self.path_log)
        # Check if the output file already exists
        if not self.log_data:
            # If it doesn't exist, create a new log_data
            self.log_data = {
                'commands': [],
                'dateStart': date_now,
                'dateLast': date_now,
                'errors': [],
                'status': LOG_STATUS_STARTED
            }

    def get_time_string(self) -> str:
        return str(datetime.datetime.now())

    def append_event(self, name, data: dict | None = None):
        log = self.kernel.current_request.log if self.kernel.current_request else self.log_data

        if 'events' not in log:
            log['events'] = []

        event = {
            'name': name
        }

        if data:
            event['data'] = data

        log['events'].append(event)

        self.write()

    def append_error(
            self,
            code: str,
            parameters=None,
            log_level: int = None):
        if parameters is None:
            parameters = {}

        # An error may occur before any command starts.
        if self.current_command:
            container = self.current_command
        else:
            container = self.log_data

        if 'errors' not in self.current_command:
            self.current_command['errors'] = []

        container['errors'].append({
            'code': code,
            'date': self.get_time_string(),
            'parameters': parameters,
            'level': log_level
        })

        self.write()

    def append_request(self, request):
        self.current_command = {
            'command': request.command,
            'date': self.get_time_string(),
        }

        self.log_data['commands'].append(
            self.current_command
        )

        self.log_data['dateLast'] = self.get_time_string()
        self.log_data['duration'] = time.time() - self.time_start

        self.write()

    def write(self):
        if (self.kernel.root_request
                and self.kernel.root_request.function
                and hasattr(self.kernel.root_request.function.callback, 'no_log')):
            return

        with open(self.path_log, 'w') as f:
            json.dump(self.log_data, f, indent=4)
            set_user_or_sudo_user_owner(self.path_log)

    def write_output(self, output: str):
        # Log stdout (which now also includes stderr)
        with open(self.path_output, 'a') as out_file:
            out_file.write(output)

    def get_all_logs_files(self) -> list:
        directory = self.kernel.get_or_create_path('log')

        all_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        json_files = [directory + f for f in all_files if f.endswith('.json')]
        return sorted(json_files)

    def find_by_command(self, command):
        all = self.get_all_logs_files()
        filtered = []

        for file in all:
            log = load_json_if_valid(file)
            if len(log['commands']):
                command_data = log['commands'][0]

                if command_data['command'] == command:
                    filtered.append(log)

        return filtered

    def find_by_function(self, function):
        return self.find_by_command(
            self.kernel.get_command_resolver(
                COMMAND_TYPE_ADDON
            ).build_command_from_function(
                function
            )
        )

    def build_summary(self, data) -> list:
        return [
            data['dateStart'],
            data['commands'][0]['command'] if len(data['commands']) else '-',
            data['status']
        ]
