from addons.test.command.demo_command.response_collection import test__demo_command__response_collection
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandDemoCommandResponseCollection(AbstractTestCase):
    def test_response_collection(self):
        response = self.kernel.run_function(
            test__demo_command__response_collection
        )

        self.assertEqual(
            response,
            None
        )
