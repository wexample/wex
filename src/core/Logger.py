import datetime
import json
import os
import time

LOG_STATUS_STARTED = 'started'


class Logger:
    current_command = None

    def __init__(self, kernel):
        self.kernel = kernel
        self.output_path = os.path.join(
            self.kernel.get_or_create_path('log'),
            kernel.task_id + '.json'
        )

        self.time_start = time.time()
        date_now = self.get_time_string()

        # Check if the output file already exists
        if os.path.exists(self.output_path):
            # If it exists, load it
            with open(self.output_path, 'r') as f:
                self.log_data = json.load(f)
        else:
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

    def append_event(self, parameters):
        if not 'events' in self.current_command:
            self.current_command['events'] = []
            
        self.current_command['events'].append(parameters)

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

        container['errors'].append({
            'code': code,
            'date': self.get_time_string(),
            'parameters': parameters,
            'level': log_level
        })

        self.write()

    def append_request(self, request):
        if hasattr(request.function.callback, 'no_log') and os.geteuid() != 0:
            return

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
        from src.helper.file import set_user_or_sudo_user_owner

        with open(self.output_path, 'w') as f:
            json.dump(self.log_data, f, indent=4)
            set_user_or_sudo_user_owner(self.output_path)

    def get_all_logs_files(self) -> list:
        directory = self.kernel.get_or_create_path('log')

        all_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        json_files = [directory + f for f in all_files if f.endswith('.json')]
        return sorted(json_files)
