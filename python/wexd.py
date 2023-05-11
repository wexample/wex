#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import re
import os
import subprocess

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        url = urlparse(self.path)
        self.parse_url(url)

    def get_env(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.dirname(current_directory)

        return self.get_env_var(
            os.path.join(parent_directory, ".wex", ".env"),
            "APP_ENV"
        )

    def get_env_var(self, env_file_path, variable_name):
        with open(env_file_path, "r") as file:
            for line in file:
                key, value = line.strip().split("=", 1)
                if key == variable_name:
                    return value

        return None

    def execute_command(self, command, working_directory):
        subprocess.Popen(command, cwd=working_directory)

    def parse_url(self, parsed_url):
        path = parsed_url.path
        pattern = r'^\/webhook/([a-zA-Z]+)/([a-zA-Z]+)$'
        match = re.match(pattern, path)

        if match:
            app_name, webhook = match.groups()
            query_string_data = parse_qs(parsed_url.query)

            env = self.get_env()
            working_directory = f"/var/www/{env}/{app_name}"
            hook_file = f".wex/webhook/{webhook}.sh"

            if os.path.isdir(working_directory) and os.path.isfile(os.path.join(working_directory, hook_file)):
                self.execute_command(['bash', hook_file], working_directory)
                self.wfile.write(b'RUNNING')
            else:
                self.wfile.write(b'NOT_FOUND')

def serve(port):
    with HTTPServer(('', port), handler) as server:
        server.serve_forever()

if __name__ == "__main__":
    serve(4242)
