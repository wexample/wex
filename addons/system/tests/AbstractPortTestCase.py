import socket
from multiprocessing import Process

from tests.AbstractTestCase import AbstractTestCase


class AbstractPortTestCase(AbstractTestCase):
    def start_temp_server(self, port: int = 45678) -> None:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("localhost", port))
        server_socket.listen(1)
        self.log(f"Listening on port {port}")

        while True:
            client_socket, address = server_socket.accept()
            self.log(f"Accepted connection from {address}")
            client_socket.close()

    def stop_test_process(self, server_process: Process) -> None:
        server_process.terminate()
        server_process.join()

    def start_test_process(self, port: int) -> Process:
        server_process = Process(target=self.start_temp_server, args=(port,))
        server_process.start()

        return server_process
