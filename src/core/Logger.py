import datetime
import json
import os
import time

from src.helper.file import set_user_or_sudo_user_owner
from src.helper.json import load_json_if_valid, parse_json_if_valid
from src.const.globals import COMMAND_TYPE_ADDON
from src.core.FunctionProperty import FunctionProperty

LOG_STATUS_COMPLETE = 'complete'
LOG_STATUS_STARTED = 'started'


class Logger:
    current_command = None

    def __init__(self, kernel):
        self.kernel = kernel

        self.time_start = time.time()
        date_now = self.get_time_string()

        self.log_data = self.load_logs(self.kernel.task_id)

        # Check if the output file already exists
        if not self.log_data:
            # If it doesn't exist, create a new log_data
            self.log_data = {
                'task_id': kernel.task_id,
                'commands': [],
                'dateStart': date_now,
                'dateLast': date_now,
                'errors': [],
                'children': {},
                'status': LOG_STATUS_STARTED,
                'parent_task_id': self.kernel.parent_task_id
            }

        if self.kernel.parent_task_id:
            parent_logs = self.load_logs(self.kernel.parent_task_id)

            if parent_logs:
                parent_logs['children'][date_now] = self.kernel.task_id
                self.write(
                    task_id=self.kernel.parent_task_id,
                    log_data=parent_logs
                )

    def load_logs(self, task_id: str):
        return parse_json_if_valid(
            self.kernel.task_file_load(
                'json',
                task_id=task_id,
                delete_after_read=False
            )
        ) or {}

    def get_time_string(self) -> str:
        return str(datetime.datetime.now())

    def get_time_string(self) -> str:
        return str(datetime.datetime.now())

    def append_event(self, name, data: dict | None = None):
        if 'events' not in self.log_data:
            self.log_data['events'] = []

        event = {
            'name': name
        }

        if data:
            event['data'] = data

        self.log_data['events'].append(event)

        self.write()

    def append_error(
            self,
            code: str,
            parameters=None,
            log_level: int = None):
        if parameters is None:
            parameters = {}

        if 'errors' not in self.log_data:
            self.log_data['errors'] = []

        self.log_data['errors'].append({
            'code': code,
            'date': self.get_time_string(),
            'parameters': parameters,
            'level': log_level
        })

        self.write()

    def append_request(self, request):
        self.current_command = {
            'command': request.command,
            'args': request.args,
            'date': self.get_time_string(),
        }

        self.log_data['commands'].append(
            self.current_command
        )

        self.log_data['dateLast'] = self.get_time_string()
        self.log_data['duration'] = time.time() - self.time_start

        self.write()

    def write(self, task_id: None | str = None, log_data: dict | None = None):
        # When writing current log, check if disabled.
        if (self.kernel.root_request
                and self.kernel.root_request.function
                and FunctionProperty.has_property(self.kernel.root_request.function, name='no_log')):
            return

        log_path = self.kernel.task_file_write(
            'json',
            json.dumps(log_data or self.log_data, indent=4),
            task_id=task_id,
            replace=True
        )

        set_user_or_sudo_user_owner(log_path)

    def write_output(self, output: str):
        self.kernel.task_file_write(
            'out',
            output
        )

    def get_all_logs_files(self) -> list:
        directory = self.kernel.get_or_create_path('task')

        all_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        json_files = [directory + f for f in all_files if f.endswith('.json')]
        return sorted(json_files)

    def find_by_command(self, command):
        all = self.get_all_logs_files()
        filtered = []

        for file in all:
            log = load_json_if_valid(file)
            if log and len(log['commands']):
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

    def set_status_complete(self, task_id: str | None = None):
        if task_id:
            log_data = self.load_logs(task_id)
        else:
            task_id = self.kernel.task_id
            log_data = self.log_data

        log_data['status'] = LOG_STATUS_COMPLETE
        self.write(task_id, log_data)
