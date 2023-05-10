#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        message = "WEX"
        self.wfile.write(bytes(message, "utf8"))

def serve(port):
    with HTTPServer(('', 4242), handler) as server:
        server.serve_forever()

if __name__ == "__main__":
    serve(4242)
