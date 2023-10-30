from addons.system.tests.AbstractPortTestCase import AbstractPortTestCase
from addons.system.command.process.by_port import system__process__by_port


class TestSystemCommandProcessByPort(AbstractPortTestCase):
    def test_by_port(self):
        port = 45678
        server_process = self.start_test_process(port)

        response = self.kernel.run_function(system__process__by_port, {
            'port': port
        })

        self.assertTrue(
            f' {port} ' in response.first()
        )

        self.assertTrue(
            f' python ' in response.first()
        )

        self.stop_test_process(server_process)
