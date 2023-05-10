#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import re
import subprocess

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        url = urlparse(self.path)
        self.parse_url(url)

    def parse_url(self, parsed_url):
        path = parsed_url.path

        pattern = r'^\/webhook/([a-zA-Z]+)/([a-zA-Z]+)$'
        match = re.match(pattern, path)

        if match:
            part1, part2 = match.groups()

            query_string_data = parse_qs(parsed_url.query)

            output = subprocess.check_output(["wex", "hi"])
            self.wfile.write(output)

def serve(port):
    with HTTPServer(('', port), handler) as server:
        server.serve_forever()

if __name__ == "__main__":
    serve(4242)
