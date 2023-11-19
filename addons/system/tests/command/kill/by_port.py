from addons.system.command.kill.by_port import system__kill__by_port
from addons.system.tests.AbstractPortTestCase import AbstractPortTestCase
from src.helper.process import process_get_all_by_port


class TestSystemCommandKillByPort(AbstractPortTestCase):
    def test_by_port(self):
        port = 45678
        server_process = self.start_test_process(port)

        # Running
        process = process_get_all_by_port(port)
        self.assertIsNotNone(process)

        self.kernel.run_function(
            system__kill__by_port,
            {
                'port': port
            }
        )

        self.stop_test_process(server_process)

        # Not running
        process = process_get_all_by_port(port)
        self.assertIsNone(process)
