from addons.test.command.demo_command.counting_collection import (
    test__demo_command__counting_collection,
)
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandDemoCommandCountingCollection(AbstractTestCase):
    def test_counting_collection(self) -> None:
        response = self.kernel.run_function(
            test__demo_command__counting_collection, {"initial": 123}
        )

        self.assertResponseFirstEqual(response, 123)

        self.assertResponseOutputBagItemContains(response, 1, 124)
