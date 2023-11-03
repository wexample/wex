from addons.test.command.logging.event import test__logging__event
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandLoggingEvent(AbstractTestCase):
    def test_event(self):
        self.kernel.run_function(test__logging__event)

        self.assertTrue(
            'events' in self.kernel.logger.log_data['commands'][0]
        )
