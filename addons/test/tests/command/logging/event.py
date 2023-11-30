from addons.test.command.logging.event import test__logging__event
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandLoggingEvent(AbstractTestCase):
    def test_event(self) -> None:
        self.kernel.run_function(test__logging__event)
        has_empty_event = False
        has_event_with_data = False

        for event in self.kernel.logger.log_data["events"]:
            if event["name"] == "TEST_EVENT_EMPTY":
                has_empty_event = True
            if event["name"] == "TEST_EVENT_DATA":
                has_event_with_data = True

        self.assertTrue(has_empty_event)

        self.assertTrue(has_event_with_data)
