from addons.system.command.process.by_port import system__process__by_port
from addons.system.tests.AbstractPortTestCase import AbstractPortTestCase


class TestSystemCommandProcessByPort(AbstractPortTestCase):
    def test_by_port(self, port: int = 45678) -> None:
        server_process = self.start_test_process(port)

        response = self.kernel.run_function(system__process__by_port, {"port": port})

        self.assertResponseFirstContains(response, f" {port}")

        self.assertResponseFirstContains(response, f" python")

        self.stop_test_process(server_process)
