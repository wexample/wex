import datetime
import json
import os
import time


class Logger:
    current_command = None

    def __init__(self, kernel):
        self.kernel = kernel
        self.output_path = os.path.join(
            self.kernel.path['log'],
            datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f') + '.json'
        )

        self.time_start = time.time()

        date_now = self.get_time_string()
        self.log_data = {
            'dateStart': date_now,
            'dateLast': date_now,
            'commands': [],
            'errors': [],
        }

        os.makedirs(self.kernel.path['log'], exist_ok=True)

    def get_time_string(self) -> str:
        return str(datetime.datetime.now())

    def append_event(self, parameters):
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
        self.current_command = {
            'command': request.command,
            'date': self.get_time_string(),
            'errors': [],
            'events': [],
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
