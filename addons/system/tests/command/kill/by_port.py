from addons.system.command.kill.by_port import system__kill__by_port
from src.helper.system import get_processes_by_port
from tests.AbstractTestCase import AbstractTestCase
from multiprocessing import Process
import socket


class TestSystemCommandKillByPort(AbstractTestCase):
    def start_temp_server(self, port: int):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', port))
        server_socket.listen(1)
        self.log(f"Listening on port {port}")

        while True:
            client_socket, address = server_socket.accept()
            self.log(f"Accepted connection from {address}")
            client_socket.close()

    def test_by_port(self):
        port = 45678

        server_process = Process(target=self.start_temp_server, args=(port,))
        server_process.start()

        # Running
        process = get_processes_by_port(port)
        self.assertIsNotNone(process)

        self.kernel.run_function(
            system__kill__by_port,
            {
                'port': port
            }
        )

        server_process.terminate()
        server_process.join()

        # Not running
        process = get_processes_by_port(port)
        self.assertIsNone(process)
